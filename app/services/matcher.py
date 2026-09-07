import re
from typing import List

from app.services.embedding import calculate_embedding_similarity


COMMON_SKILLS = {
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "sql",
    "html",
    "css",
    "react",
    "node.js",
    "express.js",
    "fastapi",
    "flask",
    "django",
    "mongodb",
    "mysql",
    "postgresql",
    "sqlite",
    "supabase",
    "sqlalchemy",
    "git",
    "docker",
    "dockerode",
    "aws",
    "azure",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "machine learning",
    "deep learning",
    "llm",
    "llms",
    "transformers",
    "prompt engineering",
    "rest api",
    "rest apis",
    "electron",
    "tailwind css",
    "bootstrap",
    "chart.js",
    "graphviz",
    "flex",
    "bison",
    "data structures",
    "algorithms",
    "object-oriented programming",
    "compiler design",
    "parsing",
    "semantic analysis",
}


def extract_jd_skills(job_description: str) -> List[str]:
    text = job_description.lower()
    found_skills = []

    for skill in COMMON_SKILLS:

        if skill == "c":
            pattern = r"(?<![a-z0-9])c(?![a-z0-9])"
        else:
            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(skill.lower())
                + r"(?![a-z0-9])"
            )

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(found_skills)


def calculate_skill_match(
    candidate_skills: List[str],
    required_skills: List[str],
) -> dict:
    candidate_set = {
        skill.lower().strip()
        for skill in candidate_skills
    }

    required_set = {
        skill.lower().strip()
        for skill in required_skills
    }

    if not required_set:
        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = sorted(
        candidate_set.intersection(required_set)
    )

    missing = sorted(
        required_set - candidate_set
    )

    score = (
        len(matched) / len(required_set)
    ) * 100

    return {
        "score": round(score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
    }


def calculate_text_similarity(
    candidate_text: str,
    job_description: str,
) -> float:
    return calculate_embedding_similarity(
        candidate_text,
        job_description,
    )


def calculate_experience_score(
    experience: str | None,
    projects: str | None,
    job_description: str,
) -> float:
    experience_score = 0.0
    project_score = 0.0

    if experience and experience.strip():
        experience_score = calculate_text_similarity(
            experience,
            job_description,
        )

    if projects and projects.strip():
        project_score = calculate_text_similarity(
            projects,
            job_description,
        )

    if experience_score > 0 and project_score > 0:
        return round(
            (experience_score * 0.7)
            + (project_score * 0.3),
            2,
        )

    return round(
        max(experience_score, project_score),
        2,
    )


def calculate_education_score(
    education: str | None,
    job_description: str,
) -> float:
    if not education or not education.strip():
        return 0.0

    return calculate_text_similarity(
        education,
        job_description,
    )


def calculate_weighted_score(
    skill_score: float,
    semantic_score: float,
    experience_score: float,
    education_score: float,
) -> float:
    final_score = (
        (skill_score * 0.50)
        + (semantic_score * 0.25)
        + (experience_score * 0.15)
        + (education_score * 0.10)
    )

    return round(
        min(max(final_score, 0.0), 100.0),
        2,
    )
def match_resume_to_job(
    candidate_skills: List[str],
    job_description: str,
    candidate_text: str = "",
    experience: str | None = None,
    projects: str | None = None,
    education: str | None = None,
) -> dict:
    required_skills = extract_jd_skills(
        job_description
    )

    skill_result = calculate_skill_match(
        candidate_skills,
        required_skills,
    )

    semantic_score = calculate_text_similarity(
        candidate_text,
        job_description,
    )

    experience_score = calculate_experience_score(
        experience,
        projects,
        job_description,
    )

    education_score = calculate_education_score(
        education,
        job_description,
    )

    final_score = calculate_weighted_score(
        skill_score=skill_result["score"],
        semantic_score=semantic_score,
        experience_score=experience_score,
        education_score=education_score,
    )

    return {
        "required_skills": required_skills,
        "skill_match_score": skill_result["score"],
        "semantic_similarity_score": semantic_score,
        "experience_score": experience_score,
        "education_score": education_score,
        "match_score": final_score,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
    }