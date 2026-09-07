from pathlib import Path

import fitz
from docx import Document


ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def extract_text_from_pdf(file_path: str) -> str:
    text = []

    with fitz.open(file_path) as pdf:
        for page in pdf:
            text.append(page.get_text())

    return "\n".join(text).strip()


def extract_text_from_docx(file_path: str) -> str:
    document = Document(file_path)

    paragraphs = [paragraph.text for paragraph in document.paragraphs]

    return "\n".join(paragraphs).strip()


def extract_resume_text(file_path: str) -> str:
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}. "
        "Only PDF and DOCX files are supported."
    )