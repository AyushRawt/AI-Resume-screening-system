from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.screening_result import ScreeningResult


router = APIRouter(
    prefix="/screening-results",
    tags=["Screening Results"],
)


@router.get("/")
def get_screening_results(
    db: Session = Depends(get_db),
):
    results = (
        db.query(ScreeningResult)
        .order_by(ScreeningResult.match_score.desc())
        .all()
    )

    return [
        {
            "id": result.id,
            "candidate_id": result.candidate_id,
            "job_id": result.job_id,
            "skill_match_score": result.skill_match_score,
            "semantic_similarity_score": result.semantic_similarity_score,
            "experience_score": result.experience_score,
            "education_score": result.education_score,
            "match_score": result.match_score,
            "matched_skills": result.matched_skills,
            "missing_skills": result.missing_skills,
        }
        for result in results
    ]