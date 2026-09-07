from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from app.database.database import Base


class ScreeningResult(Base):
    __tablename__ = "screening_results"

    id = Column(Integer, primary_key=True, index=True)

    candidate_id = Column(
        Integer,
        ForeignKey("candidates.id"),
        nullable=False,
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False,
    )

    skill_match_score = Column(Float, nullable=False, default=0.0)
    semantic_similarity_score = Column(Float, nullable=False, default=0.0)
    experience_score = Column(Float, nullable=False, default=0.0)
    education_score = Column(Float, nullable=False, default=0.0)

    match_score = Column(Float, nullable=False, default=0.0)

    matched_skills = Column(JSONB, nullable=False, default=list)
    missing_skills = Column(JSONB, nullable=False, default=list)