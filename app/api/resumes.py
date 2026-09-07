import os
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.resume_parser import extract_resume_text
from app.services.extractor import extract_candidate_info


router = APIRouter(prefix="/resumes", tags=["Resumes"])

UPLOAD_DIR = Path("data/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    file_path = UPLOAD_DIR / file.filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = extract_resume_text(str(file_path))

        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume.",
            )

        candidate = extract_candidate_info(extracted_text)

        return {
            "filename": file.filename,
            "file_type": extension,
            "message": (
                "Resume uploaded and candidate information "
                "extracted successfully."
            ),
            "candidate": candidate,
        }

    except HTTPException:
        raise

    except Exception as exc:
        if file_path.exists():
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process resume: {str(exc)}",
        )