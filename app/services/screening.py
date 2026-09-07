from typing import List

from app.services.extractor import extract_candidate_info
from app.services.matcher import match_resume_to_job
from app.services.resume_parser import extract_resume_text


def screen_candidate(
    file_path: str,
    job_description: str,
) -> dict:
    resume_text = extract_resume_text(file_path)

    if not resume_text:
        raise ValueError("Could not extract text from resume.")

    candidate = extract_candidate_info(resume_text)

    match_result = match_resume_to_job(
        candidate_skills=candidate["skills"],
        job_description=job_description,
        candidate_text=resume_text,
        experience=candidate["experience"],
        projects=candidate["projects"],
        education=candidate["education"],
    )

    return {
        "filename": file_path.split("\\")[-1],
        "name": candidate["name"],
        "email": candidate["email"],
        "phone": candidate["phone"],
        "skills": candidate["skills"],
        "education": candidate["education"],
        "experience": candidate["experience"],
        "projects": candidate["projects"],
        "certifications": candidate["certifications"],

        "match_score": match_result["match_score"],

        "skill_match_score": match_result["skill_match_score"],
        "semantic_similarity_score": match_result["semantic_similarity_score"],
        "experience_score": match_result["experience_score"],
        "education_score": match_result["education_score"],

        "required_skills": match_result["required_skills"],
        "matched_skills": match_result["matched_skills"],
        "missing_skills": match_result["missing_skills"],
    }


def rank_candidates(candidates: List[dict]) -> List[dict]:
    ranked = sorted(
        candidates,
        key=lambda candidate: candidate["match_score"],
        reverse=True,
    )

    for rank, candidate in enumerate(ranked, start=1):
        candidate["rank"] = rank

    return ranked