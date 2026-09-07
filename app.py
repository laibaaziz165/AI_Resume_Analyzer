import streamlit as st
import pandas as pd

from resume_parser import extract_text_from_pdf
from ai_analyzer import analyze_resume, parse_ai_response

# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SESSION STATE
if "results_df" not in st.session_state:
    st.session_state.results_df = None

if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

# SIDEBAR
with st.sidebar:
    st.title("📄 AI Resume Analyzer")
    st.write(
        "Smart resume screening for modern recruitment."
    )
    st.divider()
    st.subheader("🚀 Features")
    st.markdown(
        """
        ✅ PDF resume extraction

        ✅ AI-powered resume matching

        ✅ Fit score from 0–100

        ✅ Strength & skill gap analysis

        ✅ Batch resume processing

        ✅ Automatic candidate ranking

        ✅ CSV shortlist export
        """
    )
    st.divider()
    st.caption(
        "Built with Python • Streamlit • AI"
    )

# HEADER
st.title("📄 AI Resume Analyzer")
st.write(
    "AI-powered resume screening that helps recruiters "
    "identify the best candidates faster."
)
st.divider()

# INPUT SECTION
st.subheader("🎯 Start Screening")
col1, col2 = st.columns([1, 1.4])

# RESUME UPLOAD
with col1:
    st.markdown("### 📂 Upload Resumes")
    uploaded_files = st.file_uploader(
        "Upload one or more candidate resumes",
        type=["pdf"],
        accept_multiple_files=True,
        help="PDF format only. You can upload multiple resumes."
    )
    if uploaded_files:
        st.success(
            f"✅ {len(uploaded_files)} resume(s) uploaded"
        )
        for file in uploaded_files:
            st.caption(
                f"📄 {file.name}"
            )

# JOB DESCRIPTION
with col2:
    st.markdown("### 💼 Job Description")
    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder=(
            "Example:\n\n"
            "We are looking for an AI/ML Engineer with experience "
            "in Python, Machine Learning, Scikit-learn, Pandas, "
            "NumPy, SQL, NLP and data analysis..."
        ),
        help="Paste the complete job description here."
    )
    if job_description.strip():
        word_count = len(
            job_description.split()
        )
        st.caption(
            f"📝 Job description: {word_count} words"
        )
st.divider()

# ANALYZE BUTTON
analyze_button = st.button(
    "🔍 Analyze Candidates",
    type="primary",
    use_container_width=True
)

# ANALYZE RESUMES
if analyze_button:
  
    # INPUT VALIDATION
    if not uploaded_files:
        st.warning(
            "📂 Please upload at least one resume."
        )
    elif not job_description.strip():
        st.warning(
            "💼 Please enter a job description."
        )
    else:
        results = []
        errors = []
        progress_bar = st.progress(0)
        total_files = len(uploaded_files)

        # PROCESS EACH RESUME
        for index, uploaded_file in enumerate(
            uploaded_files
        ):
            try:
                with st.spinner(
                    f"Analyzing {uploaded_file.name}..."
                ):

                    # Extract resume text
                    resume_text = extract_text_from_pdf(
                        uploaded_file
                    )


                    # Check extracted text
                    if (
                        not resume_text
                        or not resume_text.strip()
                    ):
                        errors.append(
                            f"{uploaded_file.name}: "
                            "No readable text could be extracted."
                        )
                        continue

                    # AI analysis
                    result = analyze_resume(
                        resume_text,
                        job_description
                    )

                    # Check AI response
                    if (
                        not result
                        or not result.strip()
                    ):
                        errors.append(
                            f"{uploaded_file.name}: "
                            "AI analysis returned no result."
                        )
                        continue

                    # Parse AI response
                    parsed_result = parse_ai_response(
                        result
                    )

                    # Validate fit score
                    score = parsed_result[
                        "fit_score"
                    ]
                    try:
                        score = int(score)
                    except (
                        ValueError,
                        TypeError
                    ):
                        score = 0
                    if score < 0 or score > 100:
                        score = 0

                    # Store result
                    results.append(
                        {
                            "Candidate":
                                uploaded_file.name,

                            "Fit Score":
                                score,

                            "Recommendation":
                                parsed_result[
                                    "recommendation"
                                ],

                            "Strengths":
                                ", ".join(
                                    parsed_result[
                                        "strengths"
                                    ]
                                ),

                            "Skill Gaps":
                                ", ".join(
                                    parsed_result[
                                        "skill_gaps"
                                    ]
                                )
                        }
                    )

            except Exception as e:
                errors.append(
                    f"{uploaded_file.name}: {str(e)}"
                )
                continue

            # Update progress
            progress_bar.progress(
                (index + 1) / total_files
            )
        progress_bar.empty()

        # DISPLAY ERRORS
        if errors:
            st.warning(
                "⚠️ Some resumes could not be analyzed."
            )
            with st.expander(
                "View Processing Errors"
            ):
                for error in errors:
                    st.write(
                        f"• {error}"
                    )

        # CHECK RESULTS
        if not results:
            st.error(
                "❌ No resumes were successfully analyzed. "
                "Please check your PDF files and try again."
            )

            st.session_state.results_df = None
            st.session_state.analysis_complete = False
        else:

            # SORT RESULTS
            results = sorted(
                results,
                key=lambda x: int(
                    x["Fit Score"]
                ),
                reverse=True
            )

            # CREATE DATAFRAME
            results_df = pd.DataFrame(
                results
            )


            # Add ranking
            results_df.insert(
                0,
                "Rank",
                range(
                    1,
                    len(results_df) + 1
                )
            )

            # SAVE RESULTS IN SESSION STATE
            st.session_state.results_df = results_df
            st.session_state.analysis_complete = True

# DISPLAY RESULTS
if (
    st.session_state.analysis_complete
    and st.session_state.results_df is not None
):
    results_df = st.session_state.results_df

    # SCREENING OVERVIEW
    st.divider()
    st.subheader(
        "📊 Screening Overview"
    )


    total_candidates = len(
        results_df
    )

    average_score = round(
        results_df[
            "Fit Score"
        ].mean()
    )

    top_score = int(
        results_df[
            "Fit Score"
        ].max()
    )

    strong_matches = len(
        results_df[
            results_df[
                "Recommendation"
            ].isin(
                [
                    "Strong Match",
                    "Good Match"
                ]
            )
        ]
    )

    metric1, metric2, metric3, metric4 = st.columns(4)
    with metric1:
        st.metric(
            "👥 Candidates",
            total_candidates
        )

    with metric2:
        st.metric(
            "📈 Average Score",
            f"{average_score}/100"
        )

    with metric3:
        st.metric(
            "🏆 Highest Score",
            f"{top_score}/100"
        )

    with metric4:
        st.metric(
            "⭐ Strong Matches",
            strong_matches
        )

    # RANKED CANDIDATES
    st.divider()
    st.subheader(
        "🏆 Ranked Candidates"
    )
    st.caption(
        "Candidates are automatically ranked "
        "from highest to lowest fit score."
    )
    st.dataframe(
        results_df[
            [
                "Rank",
                "Candidate",
                "Fit Score",
                "Recommendation"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


    # DETAILED CANDIDATE ANALYSIS
    st.divider()
    st.subheader(
        "🔎 Candidate Analysis"
    )
    st.write(
        "Select a candidate to view their "
        "AI-generated strengths and skill gaps."
    )

    candidate_names = results_df[
        "Candidate"
    ].tolist()


    selected_candidate = st.selectbox(
        "Select Candidate",
        candidate_names,
        key="selected_candidate"
    )


    # Find selected candidate
    candidate_data = results_df[
        results_df[
            "Candidate"
        ] == selected_candidate
    ].iloc[0]


    # CANDIDATE INFORMATION

    info_col1, info_col2 = st.columns(2)

    with info_col1:

        st.markdown("### 📄 Candidate")

        st.info(
            candidate_data[
                "Candidate"
            ]
        )

    with info_col2:

        st.markdown("### 📊 Fit Score")

        st.metric(
            "Overall Match",
            f"{candidate_data['Fit Score']}/100"
        )

    # Score progress bar
    st.progress(
        int(
            candidate_data[
                "Fit Score"
            ]
        ) / 100
    )

    # RECOMMENDATION
    st.markdown("### 🎯 Recommendation")

    recommendation = candidate_data[
        "Recommendation"
    ]

    if recommendation == "Strong Match":

        st.success(
            f"⭐ {recommendation}"
        )

    elif recommendation == "Good Match":

        st.success(
            f"✅ {recommendation}"
        )

    elif recommendation == "Consider with Reservations":

        st.warning(
            f"⚠️ {recommendation}"
        )

    else:

        st.error(
            f"❌ {recommendation}"
        )


    # STRENGTHS & SKILL GAPS
    detail_col1, detail_col2 = st.columns(2)

    # Strengths
    with detail_col1:

        st.markdown("### 💪 Strengths")

        strengths = candidate_data[
            "Strengths"
        ]

        if strengths:
            for strength in strengths.split(
                ", "
            ):

                st.success(
                    f"✓ {strength}"
                )
        else:
            st.info(
                "No strengths were identified."
            )

    # Skill gaps

    with detail_col2:

        st.markdown("### ⚠️ Skill Gaps")

        skill_gaps = candidate_data[
            "Skill Gaps"
        ]

        if skill_gaps:

            for gap in skill_gaps.split(
                ", "
            ):

                st.warning(
                    f"• {gap}"
                )

        else:

            st.info(
                "No significant skill gaps were identified."
            )


    # CSV EXPORT

    st.divider()
    st.subheader(
        "📥 Export Results"
    )

    st.write(
        "Download the complete ranked shortlist "
        "including strengths and skill gaps."
    )

    csv_data = results_df.to_csv(
        index=False
    )
    st.download_button(
        label="📥 Download Ranked Shortlist",
        data=csv_data,
        file_name="ranked_resume_shortlist.csv",
        mime="text/csv",
        use_container_width=True
    )

# FOOTER
st.divider()
st.caption(
    "AI Resume Analyzer • Intelligent Candidate Screening"
)