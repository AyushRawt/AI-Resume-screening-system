from fastapi import FastAPI

from app.api.resumes import router as resume_router
from app.api.jobs import router as job_router
from app.api.jobs_read import router as jobs_read_router
from app.api.screening import router as screening_router
from app.api.candidates import router as candidates_router
from app.api.results import router as results_router


app = FastAPI(
    title="AI Resume Screening System",
    description="AI-powered resume screening and candidate ranking API",
    version="1.0.0",
)


app.include_router(resume_router)
app.include_router(job_router)
app.include_router(jobs_read_router)
app.include_router(screening_router)
app.include_router(candidates_router)
app.include_router(results_router)


@app.get("/")
def root():
    return {
        "message": "AI Resume Screening System API is running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
