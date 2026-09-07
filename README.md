# AI Resume Screening System (ResumeIQ)

## Overview
The AI Resume Screening System (ResumeIQ) is a web-based application designed to help recruiters efficiently screen and rank candidates against specific job descriptions. 

By accepting resumes in PDF and DOCX formats, the system automatically extracts crucial candidate information, evaluates it against the job requirements using a blend of skill-based matching and semantic similarity, and generates a comprehensive match score (0-100). This ensures that candidates are ranked based on holistic fit rather than just exact keyword matches.

## Key Features
- **Resume Parsing**: Supports automated text extraction from PDF and DOCX files.
- **Data Extraction**: Automatically identifies the candidate's name, email, phone, skills, education, experience, projects, and certifications.
- **Skill Matching**: Extracts required skills from the job description and identifies matched/missing skills in the candidate's profile.
- **Semantic Similarity**: Uses advanced NLP (`Sentence Transformers`) to gauge contextual relevance between the resume and the job description.
- **Intelligent Scoring**: Evaluates experience and education relevance to generate an overall fit score (0-100).
- **Recruiter Dashboard**: Built with Streamlit for a clean, interactive user experience.
- **Export Capabilities**: Export screening results directly to a CSV file.
- **Database Integration**: Stores candidates, jobs, and screening results securely in PostgreSQL.
- **Containerized**: Fully supported by Docker and Docker Compose for easy deployment.

## Technology Stack

### Backend
- **Python 3.11**
- **FastAPI** (REST API)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (Database)

### NLP & Processing
- **Sentence Transformers** (`all-MiniLM-L6-v2`)
- **scikit-learn**
- **PyMuPDF** & **python-docx** (Resume parsing)
- **Rule-based skill matching**

### Frontend
- **Streamlit** (Dashboard UI)

### Infrastructure & Testing
- **Docker & Docker Compose**
- **pytest** & **FastAPI TestClient**

## System Workflow
1. The recruiter pastes a job description into the dashboard.
2. One or more candidate resumes (PDF/DOCX) are uploaded.
3. The system parses the resumes and extracts structured candidate data.
4. The job description is analyzed to identify core required skills.
5. The system performs skill matching and semantic similarity checks.
6. Experience and education are evaluated for relevance.
7. An overall candidate match score is calculated.
8. The dashboard displays ranked candidates alongside detailed match insights (matched vs missing skills).
9. All results are saved to PostgreSQL and can be exported as a CSV file.

## Scoring Model
The system calculates the final candidate score by weighting different components to ensure a balanced evaluation:

| Component | Weight | Description |
|-----------|--------|-------------|
| **Skill Match** | 50% | Exact matching of required vs. possessed skills |
| **Semantic Similarity** | 25% | Contextual similarity between resume and job description |
| **Experience** | 15% | Relevance of professional experience and projects |
| **Education** | 10% | Relevance of educational background |

*Formula:*
```text
Final Score = (Skill Match × 0.50) + (Semantic Similarity × 0.25) + (Experience × 0.15) + (Education × 0.10)
```

## Setup and Installation

### Using Docker (Recommended)
1. Clone the repository:
   ```bash
   git clone https://github.com/AyushRawt/AI-Resume-screening-system.git
   cd AI-Resume-screening-system
   ```
2. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at `http://localhost:8000` and the interactive API documentation at `http://localhost:8000/docs`.

### Local Development
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Ensure you have a running PostgreSQL instance and configure your `.env` file with the correct `DATABASE_URL`.
3. Run the FastAPI backend:
   ```bash
   uvicorn app.main:app --reload
   ```
4. In a separate terminal, run the Streamlit dashboard:
   ```bash
   streamlit run frontend/dashboard.py
   ```
