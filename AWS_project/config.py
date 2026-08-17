import os
from pathlib import Path

from dotenv import load_dotenv


# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


# ---------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------

APP_NAME = os.getenv(
    "APP_NAME",
    "AWS GenAI Document Intelligence"
)

FLASK_ENV = os.getenv(
    "FLASK_ENV",
    "development"
)


# ---------------------------------------------------------
# AWS
# ---------------------------------------------------------

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-south-1"
)

S3_BUCKET = os.getenv(
    "S3_BUCKET",
    ""
)

BEDROCK_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    ""
)

BEDROCK_GUARDRAIL_ID = os.getenv(
    "BEDROCK_GUARDRAIL_ID",
    ""
)

BEDROCK_GUARDRAIL_VERSION = os.getenv(
    "BEDROCK_GUARDRAIL_VERSION",
    ""
)


# ---------------------------------------------------------
# FILES
# ---------------------------------------------------------

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# LIMITS
# ---------------------------------------------------------

MAX_UPLOAD_MB = int(
    os.getenv(
        "MAX_UPLOAD_MB",
        "20"
    )
)

MAX_CONTENT_LENGTH = (
    MAX_UPLOAD_MB * 1024 * 1024
)


# ---------------------------------------------------------
# ALLOWED FILES
# ---------------------------------------------------------

ALLOWED_EXTENSIONS = {
    "pdf"
}