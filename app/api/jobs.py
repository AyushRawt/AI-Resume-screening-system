from fastapi import APIRouter
from pydantic import BaseModel

from app.services.matcher import match_resume_to_job


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


class JobMatchRequest(BaseModel):
    job_description: str
    candidate_skills: list[str]


@router.post("/match")
def match_candidate(request: JobMatchRequest):
    return match_resume_to_job(
        candidate_skills=request.candidate_skills,
        job_description=request.job_description,
    )