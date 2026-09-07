import re
from typing import List


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


def extract_email(text: str) -> str | None:
    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text,
    )

    return match.group(0) if match else None


def extract_name(text: str) -> str | None:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    first_line = lines[0]

    if (
        len(first_line.split()) <= 5
        and not any(char.isdigit() for char in first_line)
        and "@" not in first_line
    ):
        return first_line

    return None


def extract_skills(text: str) -> List[str]:
    text_lower = text.lower()
    found_skills = []

    for skill in COMMON_SKILLS:
        skill_lower = skill.lower()

        if skill_lower == "c":
            pattern = r"(?<![a-z0-9])c(?![a-z0-9])"
        else:
            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(skill_lower)
                + r"(?![a-z0-9])"
            )

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return sorted(found_skills)


def extract_section(
    text: str,
    section_names: List[str],
) -> str | None:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    target_sections = {
        section.lower().strip().rstrip(":")
        for section in section_names
    }

    all_sections = {
        "summary",
        "profile",
        "objective",
        "education",
        "educational background",
        "academic background",
        "technical skills",
        "skills",
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship",
        "internships",
        "projects",
        "personal projects",
        "academic projects",
        "project experience",
        "certifications",
        "certificates",
        "achievements",
        "contact",
    }

    collecting = False
    collected = []

    for line in lines:
        normalized = line.lower().strip().rstrip(":")

        if normalized in target_sections:
            collecting = True
            continue

        if collecting and normalized in all_sections:
            break

        if collecting:
            collected.append(line)

    if not collected:
        return None

    return "\n".join(collected)


def extract_education(text: str) -> str | None:
    return extract_section(
        text,
        [
            "education",
            "educational background",
            "academic background",
        ],
    )


def extract_experience(text: str) -> str | None:
    return extract_section(
        text,
        [
            "experience",
            "work experience",
            "professional experience",
            "employment",
            "internship",
            "internships",
        ],
    )


def extract_projects(text: str) -> str | None:
    return extract_section(
        text,
        [
            "projects",
            "personal projects",
            "academic projects",
            "project experience",
        ],
    )


def extract_certifications(text: str) -> List[str]:
    section = extract_section(
        text,
        [
            "certifications",
            "certificates",
        ],
    )

    if not section:
        return []

    certifications = []

    for line in section.splitlines():
        cleaned = line.strip("•-– \t")

        if cleaned:
            certifications.append(cleaned)

    return certifications


def extract_candidate_info(text: str) -> dict:
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
        "certifications": extract_certifications(text),
    }