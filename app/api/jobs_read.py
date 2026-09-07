from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.job import Job


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.get("/")
def get_jobs(
    db: Session = Depends(get_db),
):
    jobs = (
        db.query(Job)
        .order_by(Job.id.desc())
        .all()
    )

    return [
        {
            "id": job.id,
            "job_description": job.job_description,
            "created_at": job.created_at,
        }
        for job in jobs
    ]