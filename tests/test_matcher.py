from app.services.matcher import (
    calculate_skill_match,
    calculate_weighted_score,
)


def test_skill_match_all_required_skills():
    candidate_skills = [
        "Python",
        "FastAPI",
        "SQL",
        "PostgreSQL",
        "Docker",
    ]

    required_skills = [
        "Python",
        "FastAPI",
        "SQL",
        "PostgreSQL",
        "Docker",
    ]

    result = calculate_skill_match(
        candidate_skills,
        required_skills,
    )

    assert result["score"] == 100.0
    assert len(result["matched_skills"]) == 5
    assert result["missing_skills"] == []


def test_skill_match_missing_skills():
    candidate_skills = [
        "Python",
        "Git",
    ]

    required_skills = [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "Docker",
    ]

    result = calculate_skill_match(
        candidate_skills,
        required_skills,
    )

    assert result["score"] == 25.0
    assert "python" in result["matched_skills"]
    assert "fastapi" in result["missing_skills"]


def test_weighted_score():
    score = calculate_weighted_score(
        skill_score=100,
        semantic_score=80,
        experience_score=70,
        education_score=60,
    )

    assert score == 86.5