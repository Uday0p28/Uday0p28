from pathlib import Path

from pypdf import PdfReader


class DocumentProcessor:
    """
    Handles PDF validation, text extraction,
    and document statistics.
    """

    @staticmethod
    def allowed_file(filename: str) -> bool:
        """
        Check whether the uploaded file is a PDF.
        """

        if not filename:
            return False

        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower()
            == "pdf"
        )

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from all PDF pages.
        """

        reader = PdfReader(file_path)

        extracted_text = []

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                extracted_text.append(
                    page_text.strip()
                )

        return "\n\n".join(
            extracted_text
        )

    @staticmethod
    def get_statistics(
        file_path: str,
        text: str
    ) -> dict:

        reader = PdfReader(file_path)

        pages = len(reader.pages)

        words = len(
            text.split()
        )

        characters = len(text)

        file_size = Path(
            file_path
        ).stat().st_size

        file_size_mb = (
            file_size / (1024 * 1024)
        )

        return {
            "pages": pages,
            "words": words,
            "characters": characters,
            "size_bytes": file_size,
            "size_mb": round(
                file_size_mb,
                2
            )
        }

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Basic text cleanup.
        """

        lines = [
            line.strip()
            for line in text.splitlines()
        ]

        lines = [
            line
            for line in lines
            if line
        ]

        return "\n".join(lines)