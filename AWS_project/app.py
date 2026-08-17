import os
import uuid

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_file
)

from werkzeug.utils import (
    secure_filename
)

from config import (
    APP_NAME,
    ALLOWED_EXTENSIONS,
    MAX_CONTENT_LENGTH,
    OUTPUT_DIR,
    S3_BUCKET,
    AWS_REGION
)

from services.document_service import (
    DocumentProcessor
)

from services.s3_service import (
    S3Service
)

from services.bedrock_service import (
    BedrockService
)

from services.langchain_service import (
    LangChainService
)


# =========================================================
# FLASK
# =========================================================

app = Flask(
    __name__
)

app.config[
    "MAX_CONTENT_LENGTH"
] = MAX_CONTENT_LENGTH


# =========================================================
# SERVICES
# =========================================================

document_processor = (
    DocumentProcessor()
)

s3_service = S3Service(
    AWS_REGION,
    S3_BUCKET
)

bedrock_service = (
    BedrockService()
)

langchain_service = None

if bedrock_service.is_configured():

    langchain_service = (
        LangChainService(
            bedrock_service.model
        )
    )


# =========================================================
# HELPERS
# =========================================================

def json_error(
    message: str,
    status: int = 400
):

    return jsonify(
        {
            "success": False,
            "error": message
        }
    ), status


def json_success(data: dict):

    return jsonify(
        {
            "success": True,
            **data
        }
    )


# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        app_name=APP_NAME
    )


@app.route("/api/health")
def health():

    return json_success(
        {
            "status": "online",
            "bedrock_configured":
                bedrock_service.is_configured(),
            "model":
                bedrock_service.get_model_name(),
            "s3_configured":
                bool(S3_BUCKET)
        }
    )


@app.route(
    "/api/analyze",
    methods=["POST"]
)
def analyze_document():

    # -----------------------------------------------------
    # Check upload
    # -----------------------------------------------------

    if "file" not in request.files:

        return json_error(
            "No PDF file was uploaded."
        )

    uploaded_file = request.files[
        "file"
    ]

    if not uploaded_file.filename:

        return json_error(
            "Please select a PDF file."
        )

    # -----------------------------------------------------
    # Validate extension
    # -----------------------------------------------------

    if not document_processor.allowed_file(
        uploaded_file.filename
    ):

        return json_error(
            "Only PDF files are supported."
        )

    # -----------------------------------------------------
    # Check Bedrock
    # -----------------------------------------------------

    if not bedrock_service.is_configured():

        return json_error(
            (
                "Amazon Bedrock is not configured. "
                "Set BEDROCK_MODEL_ID in your .env file."
            ),
            503
        )

    # -----------------------------------------------------
    # Generate unique filename
    # -----------------------------------------------------

    original_filename = secure_filename(
        uploaded_file.filename
    )

    file_id = uuid.uuid4().hex[:12]

    filename = (
        f"{file_id}_{original_filename}"
    )

    local_path = (
        os.path.join(
            "uploads",
            filename
        )
    )

    # -----------------------------------------------------
    # Save upload
    # -----------------------------------------------------

    try:

        uploaded_file.save(
            local_path
        )

        # -------------------------------------------------
        # Extract text
        # -------------------------------------------------

        text = (
            document_processor
            .extract_text(local_path)
        )

        text = (
            document_processor
            .clean_text(text)
        )

        if not text.strip():

            return json_error(
                (
                    "No readable text was found "
                    "in this PDF. Scanned PDFs may "
                    "require OCR."
                )
            )

        # -------------------------------------------------
        # Statistics
        # -------------------------------------------------

        statistics = (
            document_processor
            .get_statistics(
                local_path,
                text
            )
        )

        # -------------------------------------------------
        # Upload to S3
        # -------------------------------------------------

        s3_key = (
            f"documents/{filename}"
        )

        s3_uri = (
            s3_service.upload_file(
                local_path,
                s3_key
            )
        )

        # -------------------------------------------------
        # Generate AI summary
        # -------------------------------------------------

        summary = (
            bedrock_service.summarize(
                langchain_service,
                text
            )
        )

        # -------------------------------------------------
        # Save summary
        # -------------------------------------------------

        summary_filename = (
            f"{file_id}_summary.txt"
        )

        summary_path = (
            OUTPUT_DIR
            / summary_filename
        )

        summary_path.write_text(
            summary,
            encoding="utf-8"
        )

        return json_success(
            {
                "document": {
                    "id": file_id,
                    "name":
                        original_filename,
                    "statistics":
                        statistics
                },

                "storage": {
                    "s3_uri": s3_uri
                },

                "ai": {
                    "model":
                        bedrock_service
                        .get_model_name(),

                    "summary":
                        summary
                },

                "download": (
                    f"/api/download/"
                    f"{summary_filename}"
                )
            }
        )

    except Exception as exc:

        app.logger.exception(
            "Document analysis failed"
        )

        return json_error(
            str(exc),
            500
        )


@app.route(
    "/api/download/<filename>"
)
def download_summary(filename):

    safe_filename = secure_filename(
        filename
    )

    file_path = (
        OUTPUT_DIR
        / safe_filename
    )

    if not file_path.exists():

        return json_error(
            "Summary file not found.",
            404
        )

    return send_file(
        file_path,
        as_attachment=True,
        download_name="AI_Summary.txt",
        mimetype="text/plain"
    )


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(413)
def file_too_large(error):

    return json_error(
        (
            "File is too large. "
            "Maximum allowed size is "
            f"{MAX_CONTENT_LENGTH // (1024 * 1024)} MB."
        ),
        413
    )


@app.errorhandler(500)
def internal_error(error):

    return json_error(
        "Internal server error.",
        500
    )


# =========================================================
# DEVELOPMENT SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )