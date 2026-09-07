\# AI Resume Screening System



\## Overview



The AI Resume Screening System is a web-based application designed to help recruiters screen and rank candidates against a given job description.



The system accepts resumes in PDF and DOCX formats, extracts important candidate information, compares the candidate's profile with the requirements of a job description, and generates a match score between 0 and 100.



The screening process combines skill-based matching with semantic similarity so that the ranking is not based only on exact keyword matches.



\## Key Features



\- Upload PDF resumes

\- Upload DOCX resumes

\- Extract candidate name, email, phone, skills, education, experience, projects, and certifications

\- Enter a job description

\- Identify required skills from the job description

\- Compare candidate skills with required skills

\- Identify matched skills

\- Identify missing skills

\- Calculate semantic similarity between resume and job description

\- Evaluate experience relevance

\- Evaluate education relevance

\- Generate an overall score from 0 to 100

\- Rank multiple candidates

\- Store candidates, jobs, and screening results in PostgreSQL

\- FastAPI REST API

\- Interactive Swagger/OpenAPI documentation

\- Streamlit recruiter dashboard

\- CSV export

\- Docker and Docker Compose support

\- Automated testing with pytest



\## Technology Stack



\### Backend



\- Python 3.11

\- FastAPI

\- SQLAlchemy

\- PostgreSQL



\### Resume Processing



\- PyMuPDF

\- python-docx



\### NLP and Matching



\- Sentence Transformers

\- all-MiniLM-L6-v2

\- scikit-learn

\- Rule-based skill matching



\### Frontend



\- Streamlit



\### Testing



\- pytest

\- FastAPI TestClient



\### Deployment



\- Docker

\- Docker Compose



\## System Workflow



The application follows this workflow:



1\. The recruiter enters a job description.

2\. One or more PDF or DOCX resumes are uploaded.

3\. The system extracts text from each resume.

4\. Candidate information is extracted from the resume.

5\. Required skills are identified from the job description.

6\. Candidate skills are compared with the required skills.

7\. The resume and job description are compared using semantic embeddings.

8\. Experience and education are evaluated.

9\. The individual scores are combined into a final score.

10\. Candidates are ranked from highest score to lowest score.

11\. Matched and missing skills are displayed.

12\. Screening results are stored in PostgreSQL.

13\. Results can be exported as CSV from the dashboard.



\## Scoring System



The final candidate score is calculated using four components:



| Component | Weight |

|---|---:|

| Skill Match | 50% |

| Semantic Similarity | 25% |

| Experience | 15% |

| Education | 10% |



The final score is calculated as:



```text

Final Score =

&#x20;   Skill Match × 0.50

&#x20; + Semantic Similarity × 0.25

&#x20; + Experience × 0.15

&#x20; + Education × 0.10

