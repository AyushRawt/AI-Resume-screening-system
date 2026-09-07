import io
import requests
import pandas as pd
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ResumeIQ | Candidate Screening",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background: #f4f7fb;
            color: #172b4d;
        }
        [data-testid="stAppViewContainer"] {
            background: #f4f7fb;
        }
        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #dfe6ef;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding: 30px 22px;
        }
        header {
            background: transparent !important;
        }
        footer {
            visibility: hidden;
        }
        .block-container {
            max-width: 1320px;
            padding: 38px 38px 60px;
        }
        h1, h2, h3 {
            color: #172b4d !important;
            letter-spacing: -0.025em;
        }
        h1 {
            font-size: 38px !important;
            line-height: 1.15 !important;
            margin: 0 0 8px !important;
        }
        h2 {
            font-size: 25px !important;
        }
        h3 {
            font-size: 18px !important;
        }
        p, label, .stCaption {
            color: #64748b !important;
        }
        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 22px;
            margin-bottom: 20px;
            border-bottom: 1px solid #e3e8ef;
        }
        .brand-icon {
            width: 42px;
            height: 42px;
            border-radius: 9px;
            background: #2563eb;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 21px;
            font-weight: 700;
        }
        .brand-name {
            color: #172b4d;
            font-size: 21px;
            font-weight: 750;
            line-height: 1.1;
        }
        .brand-subtitle {
            color: #7b8798;
            font-size: 12px;
            margin-top: 4px;
        }
        .sidebar-section {
            color: #94a3b8;
            font-size: 11px;
            font-weight: 750;
            letter-spacing: .11em;
            margin: 27px 0 8px 3px;
        }
        .sidebar-system {
            color: #52657f;
            font-size: 14px;
            padding: 9px 3px;
        }
        .sidebar-online {
            margin-top: 28px;
            padding: 14px;
            border: 1px solid #cfe9df;
            border-radius: 10px;
            background: #f2faf7;
        }
        .online-title {
            color: #167a5b;
            font-weight: 700;
            font-size: 13px;
        }
        .online-text {
            color: #6b7c8f;
            font-size: 11px;
            margin-top: 4px;
        }
        .sidebar-footer {
            color: #94a3b8;
            font-size: 11px;
            line-height: 1.6;
            margin-top: 28px;
        }
        .eyebrow {
            color: #2563eb;
            font-size: 11px;
            font-weight: 750;
            letter-spacing: .13em;
            text-transform: uppercase;
            margin-bottom: 9px;
        }
        .page-subtitle {
            color: #64748b;
            font-size: 16px;
            line-height: 1.55;
            margin-bottom: 0;
        }
        .hero-panel {
            background: #eaf2ff;
            border: 1px solid #d4e3fb;
            border-radius: 11px;
            padding: 17px 18px;
            min-height: 108px;
        }
        .hero-title {
            color: #172b4d;
            font-size: 16px;
            font-weight: 750;
            margin-bottom: 7px;
        }
        .hero-text {
            color: #60738f;
            font-size: 12px;
            line-height: 1.55;
        }
        .hero-rule {
            width: 48px;
            height: 4px;
            border-radius: 2px;
            background: #2563eb;
            margin-bottom: 12px;
        }
        .section-card {
            background: #ffffff;
            border: 1px solid #dfe6ef;
            border-radius: 11px;
            padding: 22px 24px;
            margin-bottom: 14px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, .025);
        }
        .section-head {
            display: flex;
            align-items: center;
            gap: 13px;
        }
        .step {
            min-width: 34px;
            height: 34px;
            border-radius: 50%;
            background: #eaf2ff;
            color: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 750;
        }
        .section-title {
            color: #172b4d;
            font-size: 18px;
            font-weight: 700;
            line-height: 1.3;
        }
        .section-help {
            color: #64748b;
            font-size: 13px;
            line-height: 1.45;
            margin-top: 3px;
        }
        div[data-baseweb="textarea"] > div,
        div[data-baseweb="input"] > div {
            border: 1px solid #d5deea !important;
            border-radius: 9px !important;
            background: #ffffff !important;
            box-shadow: none !important;
        }
        div[data-baseweb="textarea"] > div:focus-within,
        div[data-baseweb="input"] > div:focus-within {
            border-color: #7aa7ef !important;
            box-shadow: 0 0 0 2px #e5efff !important;
        }
        textarea {
            color: #172b4d !important;
        }
        [data-testid="stFileUploader"] {
            border: 1px dashed #b8cbe8;
            border-radius: 10px;
            background: #f8fbff;
            padding: 8px;
        }
        [data-testid="stFileUploaderDropzone"] {
            background: #f8fbff !important;
        }
        .stButton > button {
            border-radius: 8px;
            min-height: 44px;
            font-weight: 650;
        }
        .primary-action button {
            background: #2563eb !important;
            border: 1px solid #2563eb !important;
            color: #ffffff !important;
            width: 100%;
            min-height: 48px;
        }
        .primary-action button:hover {
            background: #1d4ed8 !important;
            border-color: #1d4ed8 !important;
        }
	.primary-action button:disabled {
 	    background: #8fb2f5 !important;
    	    border-color: #8fb2f5 !important;
    	    color: #ffffff !important;
    	    opacity: 1 !important;
    	    cursor: not-allowed !important;
	}

	.primary-action button:disabled p,
	.primary-action button:disabled span,
	.primary-action button:disabled div {
    	    color: #ffffff !important;
    	    opacity: 1 !important;
	}
        .metric-card, .candidate-card, .about-box {
            background: #ffffff;
            border: 1px solid #dfe6ef;
            border-radius: 10px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, .025);
        }
        .metric-card {
            padding: 17px 18px;
            min-height: 100px;
        }
        .metric-label {
            color: #64748b;
            font-size: 12px;
            margin-bottom: 7px;
        }
        .metric-value {
            color: #172b4d;
            font-size: 28px;
            font-weight: 750;
        }
        .candidate-card {
            padding: 18px 20px;
            margin-bottom: 10px;
        }
        .candidate-name {
            color: #172b4d;
            font-size: 17px;
            font-weight: 700;
        }
        .candidate-meta, .rank {
            color: #64748b;
            font-size: 12px;
        }
        .candidate-meta {
            margin-top: 4px;
        }
        .score {
            color: #2563eb;
            font-size: 24px;
            font-weight: 750;
            text-align: right;
        }
        .rank {
            font-weight: 700;
            margin-bottom: 3px;
        }
        .tag, .missing-tag {
            display: inline-block;
            padding: 4px 8px;
            margin: 3px 4px 3px 0;
            border-radius: 5px;
            font-size: 11px;
        }
        .tag {
            background: #edf4ff;
            color: #2457a6;
        }
        .missing-tag {
            background: #fff5e9;
            color: #a65d16;
        }
        .about-box {
            padding: 22px 24px;
            margin-bottom: 18px;
        }
        .about-step {
            color: #2563eb;
            font-weight: 750;
            font-size: 11px;
            letter-spacing: .08em;
            margin-bottom: 7px;
        }
        [data-testid="stDataFrame"] {
            border: 1px solid #dfe6ef;
            border-radius: 9px;
        }
    
        .block-container {
            max-width: 1280px;
            padding: 30px 34px 46px;
        }

        .section-card {
            padding: 18px 20px;
            margin-bottom: 10px;
        }

        .section-head {
            gap: 11px;
        }

        .section-help {
            font-size: 12px;
        }

        [data-testid="stFileUploader"] {
            margin-top: 0;
            padding: 5px;
        }

        .candidate-card {
            padding: 16px 18px;
            margin: 0 0 8px;
        }

        .metric-card {
            min-height: 88px;
            padding: 14px 16px;
        }

        .metric-value {
            font-size: 26px;
        }

        .candidate-name {
            font-size: 18px;
        }

        .score {
            font-size: 25px;
        }

        .stCaption {
            margin-top: 4px !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: #dfe6ef !important;
            border-radius: 12px !important;
            background: #ffffff !important;
        }

        .candidate-card + div {
            margin-top: 0 !important;
        }

        h4 {
            margin-top: 10px !important;
            margin-bottom: 6px !important;
            color: #52657f !important;
            font-size: 13px !important;
        }

        .results-divider {
            height: 1px;
            background: #e7ecf2;
            margin: 20px 0;
        }

.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"] {
    background: #2563eb !important;
    background-color: #2563eb !important;
    color: #ffffff !important;
    border: 1px solid #2563eb !important;
    font-weight: 600 !important;
    min-height: 48px !important;
    border-radius: 9px !important;
    box-shadow: none !important;
    opacity: 1 !important;
}

.stButton > button[kind="primary"] *,
[data-testid="stBaseButton-primary"] * {
    color: #ffffff !important;
    opacity: 1 !important;
}

.stButton > button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover {
    background: #1d4ed8 !important;
    background-color: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
    color: #ffffff !important;
}

.stButton > button[kind="primary"]:hover *,
[data-testid="stBaseButton-primary"]:hover * {
    color: #ffffff !important;
}

.stButton > button[kind="primary"]:focus,
.stButton > button[kind="primary"]:active,
[data-testid="stBaseButton-primary"]:focus,
[data-testid="stBaseButton-primary"]:active {
    background: #1d4ed8 !important;
    background-color: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
    color: #ffffff !important;
}

.stButton > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    border-color: #1d4ed8 !important;
}

.stButton > button[kind="primary"]:focus,
.stButton > button[kind="primary"]:active {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    border-color: #1d4ed8 !important;
}
</style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">R</div>
            <div>
                <div class="brand-name">ResumeIQ</div>
                <div class="brand-subtitle">AI-Powered Resume Screening</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        ["Screen Candidates", "About"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-section">SYSTEM</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-system">FastAPI backend</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-system">Semantic matching</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-system">PostgreSQL database</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sidebar-online">
            <div class="online-title">System Online</div>
            <div class="online-text">Resume screening services are ready.</div>
        </div>
        <div class="sidebar-footer">
            ResumeIQ v1.0<br>
            Built for smarter hiring
        </div>
        """,
        unsafe_allow_html=True,
    )

def api_screen(job_description, uploaded_files):
    multipart_files = []

    for uploaded_file in uploaded_files:
        multipart_files.append(
            (
                "files",
                (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type or "application/octet-stream",
                ),
            )
        )

    response = requests.post(
        f"{API_BASE_URL}/screen/",
        data={"job_description": job_description},
        files=multipart_files,
        timeout=300,
    )

    response.raise_for_status()
    return response.json()

def score_label(score):
    if score >= 75:
        return "Strong match"
    if score >= 50:
        return "Good match"
    if score >= 30:
        return "Partial match"
    return "Low match"

def tags_html(items, missing=False):
    if not items:
        return '<span style="color:#94a3b8;font-size:12px;">None</span>'

    css_class = "missing-tag" if missing else "tag"
    return "".join(
        f'<span class="{css_class}">{item}</span>'
        for item in items
    )

if page == "Screen Candidates":
    header_left, header_right = st.columns([1.75, 1], gap="large")
    with header_left:
        st.markdown('<div class="eyebrow">Candidate Screening</div>', unsafe_allow_html=True)
        st.title("Screen Candidates")
        st.markdown(
            '<div class="page-subtitle">Define the position, upload resumes, and review ranked candidates in one place.</div>',
            unsafe_allow_html=True,
        )
    with header_right:
        st.markdown(
            """
            <div class="hero-panel">
                <div class="hero-rule"></div>
                <div class="hero-title">Find the right talent faster</div>
                <div class="hero-text">Screen, compare and rank candidates using consistent scoring.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown(
        """
        <div class="section-card">
            <div class="section-head">
                <div class="step">1</div>
                <div>
                    <div class="section-title">Position requirements</div>
                    <div class="section-help">
                        Paste the job description used to evaluate candidate fit.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    job_description = st.text_area(
        "Job description",
        placeholder=(
            "Example: We are looking for a Python Backend Developer with "
            "experience in Python, FastAPI, SQL, PostgreSQL, Docker, Git, "
            "REST APIs and Machine Learning."
        ),
        height=170,
        max_chars=2000,
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="section-card">
            <div class="section-head">
                <div class="step">2</div>
                <div>
                    <div class="section-title">Candidate resumes</div>
                    <div class="section-help">
                        Upload multiple PDF or DOCX resumes. They will be evaluated against the position above.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Upload resumes",
        type=["pdf", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        help="PDF and DOCX files are supported.",
    )

    if uploaded_files:
        st.caption(
            f"{len(uploaded_files)} resume(s) selected"
        )

    st.markdown('<div class="primary-action">', unsafe_allow_html=True)
    analyze = st.button(
        "Analyze & Rank Candidates",
        type="primary",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze:
        if not job_description.strip():
            st.error("Please enter a job description.")
        elif not uploaded_files:
            st.error("Please upload at least one PDF or DOCX resume.")
        else:
            try:
                with st.spinner("Analyzing resumes and calculating candidate fit..."):
                    result = api_screen(job_description.strip(), uploaded_files)

                st.session_state["screening_result"] = result
                st.success(
                    f"Screening complete. {result.get('total_candidates', 0)} candidate(s) evaluated."
                )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the FastAPI backend. "
                    "Make sure the backend is running on http://127.0.0.1:8000."
                )
            except requests.exceptions.HTTPError as exc:
                detail = exc.response.text if exc.response is not None else str(exc)
                st.error(f"Screening request failed: {detail}")
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")

    result = st.session_state.get("screening_result")

    if result:
        st.markdown('<div class="eyebrow">Screening results</div>', unsafe_allow_html=True)
        st.subheader("Ranked candidates")

        candidates = result.get("candidates", [])

        if candidates:
            strong_matches = sum(
                1 for candidate in candidates
                if candidate.get("match_score", 0) >= 75
            )
            average_score = sum(
                candidate.get("match_score", 0)
                for candidate in candidates
            ) / len(candidates)

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Candidates screened</div>
                        <div class="metric-value">{len(candidates)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with c2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Strong matches</div>
                        <div class="metric-value">{strong_matches}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with c3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">Average fit score</div>
                        <div class="metric-value">{average_score:.1f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            table_rows = []
            for candidate in candidates:
                table_rows.append(
                    {
                        "Rank": candidate.get("rank"),
                        "Candidate": candidate.get("name") or "Unknown",
                        "Email": candidate.get("email") or "—",
                        "Match score": candidate.get("match_score", 0),
                        "Skill match": candidate.get("skill_match_score", 0),
                        "Semantic": candidate.get("semantic_similarity_score", 0),
                        "Experience": candidate.get("experience_score", 0),
                    }
                )

            df = pd.DataFrame(table_rows)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Match score": st.column_config.ProgressColumn(
                        "Match score",
                        min_value=0,
                        max_value=100,
                        format="%.1f",
                    ),
                    "Skill match": st.column_config.NumberColumn(
                        "Skill match",
                        format="%.1f",
                    ),
                    "Semantic": st.column_config.NumberColumn(
                        "Semantic",
                        format="%.1f",
                    ),
                    "Experience": st.column_config.NumberColumn(
                        "Experience",
                        format="%.1f",
                    ),
                },
            )

            st.subheader("Candidate details")

            selected_name = st.selectbox(
                "Select a candidate",
                [
                    candidate.get("name") or f"Candidate {candidate.get('rank')}"
                    for candidate in candidates
                ],
                label_visibility="collapsed",
            )

            selected = next(
                (
                    candidate
                    for candidate in candidates
                    if (candidate.get("name") or f"Candidate {candidate.get('rank')}")
                    == selected_name
                ),
                candidates[0],
            )

            with st.container(border=True):
                left, right = st.columns([3.2, 1], gap="large")

                with left:
                    st.markdown(
                        f"""
                        <div class="rank">RANK #{selected.get('rank', '—')}</div>
                        <div class="candidate-name">{selected.get('name') or 'Unknown candidate'}</div>
                        <div class="candidate-meta">
                            {selected.get('email') or 'No email extracted'}
                            &nbsp;&nbsp;·&nbsp;&nbsp;
                            {selected.get('phone') or 'No phone extracted'}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with right:
                    st.markdown(
                        f"""
                        <div class="candidate-meta">Overall fit</div>
                        <div class="score">{selected.get('match_score', 0):.1f}/100</div>
                        <div style="text-align:right;color:#64748b;font-size:11px;">
                            {score_label(selected.get('match_score', 0))}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                score_cols = st.columns(4, gap="small")
                score_data = [
                    ("Skill Match", selected.get("skill_match_score", 0)),
                    ("Semantic", selected.get("semantic_similarity_score", 0)),
                    ("Experience", selected.get("experience_score", 0)),
                    ("Education", selected.get("education_score", 0)),
                ]

                for col, (label, value) in zip(score_cols, score_data):
                    with col:
                        st.markdown(
                            f"""
                            <div class="score-box">
                                <div class="score-box-title">{label}</div>
                                <div class="score-box-value">{float(value):.1f}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                d1, d2 = st.columns([1, 1], gap="large")

                with d1:
                    st.markdown("#### Matched skills")
                    st.markdown(
                        tags_html(selected.get("matched_skills", [])),
                        unsafe_allow_html=True,
                    )

                    st.markdown("#### Missing skills")
                    st.markdown(
                        tags_html(selected.get("missing_skills", []), missing=True),
                        unsafe_allow_html=True,
                    )

                    st.markdown("#### Education")
                    st.write(selected.get("education") or "Not extracted")

                with d2:
                    st.markdown("#### Experience")
                    st.write(selected.get("experience") or "Not extracted")

                    st.markdown("#### Projects")
                    st.write(selected.get("projects") or "Not extracted")

                    st.markdown("#### Certifications")
                    certifications = selected.get("certifications", [])
                    if certifications:
                        for certification in certifications:
                            st.write(certification)
                    else:
                        st.write("None extracted")

            export_rows = []
            for candidate in candidates:
                export_rows.append(
                    {
                        "Rank": candidate.get("rank"),
                        "Name": candidate.get("name"),
                        "Email": candidate.get("email"),
                        "Phone": candidate.get("phone"),
                        "Match Score": candidate.get("match_score"),
                        "Skill Match Score": candidate.get("skill_match_score"),
                        "Semantic Similarity Score": candidate.get("semantic_similarity_score"),
                        "Experience Score": candidate.get("experience_score"),
                        "Education Score": candidate.get("education_score"),
                        "Matched Skills": ", ".join(candidate.get("matched_skills", [])),
                        "Missing Skills": ", ".join(candidate.get("missing_skills", [])),
                    }
                )

            export_df = pd.DataFrame(export_rows)
            csv_data = export_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Export screening results (CSV)",
                data=csv_data,
                file_name="resumeiq_screening_results.csv",
                mime="text/csv",
            )

        else:
            st.info("No candidates were returned by the screening service.")

else:
    header_left, header_right = st.columns([1.75, 1], gap="large")
    with header_left:
        st.markdown('<div class="eyebrow">Candidate Screening Platform</div>', unsafe_allow_html=True)
        st.title("ResumeIQ")
        st.markdown(
            '<div class="page-subtitle">A clean, automated workflow for evaluating resumes against a job description.</div>',
            unsafe_allow_html=True,
        )
    with header_right:
        st.markdown(
            """
            <div class="hero-panel">
                <div class="hero-rule"></div>
                <div class="hero-title">Built for practical hiring</div>
                <div class="hero-text">Structured extraction, semantic matching and ranked candidate results.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown(
        """
        <div class="about-box">
            <div class="about-step">ABOUT THE SYSTEM</div>
            <h3>AI-powered candidate screening</h3>
            <p>
                ResumeIQ extracts candidate information from resumes, compares it
                with job requirements, calculates a fit score, and ranks candidates
                for faster recruiter review.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("How it works")

    steps = [
        ("01", "Upload", "Add PDF or DOCX resumes."),
        ("02", "Extract", "Extract candidate details, skills, education, experience and projects."),
        ("03", "Match", "Compare candidate information with the job requirements using semantic matching."),
        ("04", "Rank", "Combine screening signals into a 0–100 candidate fit score."),
    ]

    cols = st.columns(4)

    for col, (number, title, description) in zip(cols, steps):
        with col:
            st.markdown(
                f"""
                <div class="about-box" style="min-height:155px;">
                    <div class="about-step">{number}</div>
                    <h3 style="margin:0 0 8px 0;">{title}</h3>
                    <p style="font-size:13px;">{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader("Scoring model")

    scoring_df = pd.DataFrame(
        [
            ["Skill Match", "50%", "Required technology and skill coverage"],
            ["Semantic Similarity", "25%", "Meaning-level similarity between resume and job"],
            ["Experience", "15%", "Relevant professional or project experience"],
            ["Education", "10%", "Educational alignment"],
        ],
        columns=["Signal", "Weight", "Purpose"],
    )

    st.dataframe(
        scoring_df,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "ResumeIQ uses FastAPI, PostgreSQL and sentence-transformer embeddings "
        "to support the screening workflow."
    )
