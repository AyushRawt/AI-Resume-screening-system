from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.candidate import Candidate


router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"],
)


@router.get("/")
def get_candidates(
    db: Session = Depends(get_db),
):
    candidates = (
        db.query(Candidate)
        .order_by(Candidate.id.desc())
        .all()
    )

    return [
        {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "skills": candidate.skills,
            "education": candidate.education,
            "experience": candidate.experience,
            "projects": candidate.projects,
            "certifications": candidate.certifications,
        }
        for candidate in candidates
    ]