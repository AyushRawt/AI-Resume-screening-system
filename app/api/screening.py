from pathlib import Path
import shutil

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.screening_result import ScreeningResult
from app.services.screening import rank_candidates, screen_candidate


router = APIRouter(
    prefix="/screen",
    tags=["Screening"],
)

UPLOAD_DIR = Path("data/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/")
async def screen_resumes(
    job_description: str = Form(...),
    files: list[UploadFile] = File(...),
):
    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    if not files:
        raise HTTPException(
            status_code=400,
            detail="At least one resume is required.",
        )

    candidates = []
    errors = []

    db: Session = SessionLocal()

    try:
        job = Job(
            job_description=job_description.strip(),
        )

        db.add(job)
        db.flush()

        for file in files:

            if not file.filename:
                errors.append(
                    "A file was uploaded without a filename."
                )
                continue

            extension = Path(file.filename).suffix.lower()

            if extension not in ALLOWED_EXTENSIONS:
                errors.append(
                    f"{file.filename}: unsupported file type. "
                    "Only PDF and DOCX are supported."
                )
                continue

            safe_filename = Path(file.filename).name
            file_path = UPLOAD_DIR / safe_filename

            try:
                with file_path.open("wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                candidate = screen_candidate(
                    file_path=str(file_path),
                    job_description=job_description,
                )

                db_candidate = Candidate(
                    name=candidate["name"],
                    email=candidate["email"],
                    phone=candidate["phone"],
                    skills=candidate["skills"],
                    education=candidate["education"],
                    experience=candidate["experience"],
                    projects=candidate["projects"],
                    certifications=candidate["certifications"],
                )

                db.add(db_candidate)
                db.flush()

                screening_result = ScreeningResult(
                    candidate_id=db_candidate.id,
                    job_id=job.id,
                    skill_match_score=candidate[
                        "skill_match_score"
                    ],
                    semantic_similarity_score=candidate[
                        "semantic_similarity_score"
                    ],
                    experience_score=candidate[
                        "experience_score"
                    ],
                    education_score=candidate[
                        "education_score"
                    ],
                    match_score=candidate["match_score"],
                    matched_skills=candidate[
                        "matched_skills"
                    ],
                    missing_skills=candidate[
                        "missing_skills"
                    ],
                )

                db.add(screening_result)

                candidates.append(candidate)

            except Exception as exc:
                errors.append(
                    f"{file.filename}: {str(exc)}"
                )

        if not candidates:
            db.rollback()

            raise HTTPException(
                status_code=400,
                detail={
                    "message": "No resumes could be processed.",
                    "errors": errors,
                },
            )

        ranked_candidates = rank_candidates(candidates)

        db.commit()

        return {
            "job_id": job.id,
            "job_description": job_description,
            "total_candidates": len(ranked_candidates),
            "candidates": ranked_candidates,
            "errors": errors,
        }

    except HTTPException:
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database operation failed: {str(exc)}",
        )

    finally:
        db.close()