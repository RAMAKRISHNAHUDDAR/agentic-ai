import html
from pathlib import Path

import streamlit as st

from app.database.database import get_student
from app.agents.risk_agent import analyze_student_risk
from app.agents.recommendation_agent import generate_recommendations
from app.memory.intervention_memory import get_intervention_history


# ============================================================
# PATHS
# ============================================================

LOGO_PATH = (
    Path(__file__).resolve().parent
    / "assets"
    / "kle_tech_logo.png"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background: #2a2020;
        color: #ffffff;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       COLLEGE HEADER
       ======================================================== */

    .college-header {
        display: flex;
        align-items: center;
        gap: 22px;

        padding: 1.2rem 1.5rem;

        background: #2a2020;

        border-bottom: 3px solid #c4161c;

        margin-bottom: 2rem;
    }

    .college-logo {
        width: 78px;
        height: auto;
        flex-shrink: 0;
    }

    .college-name {
        color: #ffffff;

        font-size: clamp(
            1.1rem,
            2vw,
            1.6rem
        );

        font-weight: 600;

        line-height: 1.4;
    }


    /* ========================================================
       HOME BUTTON
       ======================================================== */

    .home-button-area {
        margin-bottom: 1.5rem;
    }

    .home-button-area .stButton > button {
        width: auto;
        min-width: 150px;
    }


    /* ========================================================
       PAGE HEADER
       ======================================================== */

    .page-header {
        padding: 2rem 2.2rem;

        margin-bottom: 2rem;

        background: #c4161c;

        border-radius: 4px;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.25);
    }

    .page-title {
        margin: 0;

        color: #ffffff;

        font-size: clamp(
            2rem,
            4vw,
            3rem
        );

        font-weight: 700;

        line-height: 1.15;
    }

    .page-subtitle {
        margin-top: 0.8rem;

        max-width: 850px;

        color: #f8dede;

        font-size: 0.98rem;

        line-height: 1.6;
    }


    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .section-title {
        margin-top: 2rem;
        margin-bottom: 0.35rem;

        color: #ffffff;

        font-size: 1.35rem;

        font-weight: 650;
    }

    .section-subtitle {
        margin-bottom: 1.2rem;

        color: #c8bebe;

        font-size: 0.88rem;

        line-height: 1.5;
    }


    /* ========================================================
       SEARCH
       ======================================================== */

    div[data-baseweb="input"] {
        background: #ffffff;

        border-radius: 3px;

        border: 1px solid #d8d0d0;
    }

    div[data-baseweb="input"] input {
        color: #302525;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #c4161c;

        box-shadow:
            0 0 0 1px rgba(196, 22, 28, 0.25);
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        min-height: 44px;

        border-radius: 3px;

        border: 1px solid #c4161c;

        background: #c4161c;

        color: #ffffff;

        font-size: 0.9rem;

        font-weight: 600;

        transition:
            background 0.2s ease,
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        background: #a90f15;

        border-color: #a90f15;

        color: #ffffff;

        transform: translateY(-1px);

        box-shadow:
            0 7px 18px rgba(196, 22, 28, 0.30);
    }


    /* ========================================================
       INFORMATION CARDS
       ======================================================== */

    .info-card {
        padding: 1.35rem;

        min-height: 105px;

        background: #ffffff;

        border-radius: 4px;

        border-left: 5px solid #c4161c;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.20);
    }

    .card-label {
        color: #756969;

        font-size: 0.72rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }

    .card-value {
        margin-top: 0.55rem;

        color: #302525;

        font-size: 1.4rem;

        font-weight: 700;
    }


    /* ========================================================
       ACADEMIC CARDS
       ======================================================== */

    .academic-card {
        padding: 1.25rem;

        min-height: 110px;

        background: #ffffff;

        border-radius: 4px;

        border-top: 4px solid #c4161c;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.18);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .academic-card:hover {
        transform: translateY(-3px);

        box-shadow:
            0 13px 30px rgba(0, 0, 0, 0.25);
    }

    .academic-label {
        color: #756969;

        font-size: 0.72rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }

    .academic-value {
        margin-top: 0.45rem;

        color: #302525;

        font-size: 1.65rem;

        font-weight: 750;
    }


    /* ========================================================
       STATUS CARDS
       ======================================================== */

    .status-card {
        padding: 1.25rem;

        min-height: 105px;

        background: #ffffff;

        border-radius: 4px;

        border-left: 5px solid #c4161c;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.18);
    }

    .status-label {
        color: #756969;

        font-size: 0.72rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }

    .status-value {
        margin-top: 0.55rem;

        color: #302525;

        font-size: 1rem;

        font-weight: 650;
    }


    /* ========================================================
       RISK PANEL
       ======================================================== */

    .risk-panel {
        margin-top: 0.5rem;

        padding: 1.7rem;

        background: #ffffff;

        border-radius: 4px;

        border-left: 6px solid #c4161c;

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.22);
    }

    .risk-status {
        font-size: 1.9rem;

        font-weight: 800;

        letter-spacing: -0.02em;
    }

    .risk-danger {
        color: #c4161c;
    }

    .risk-safe {
        color: #287a45;
    }

    .risk-description {
        margin-top: 0.4rem;

        color: #665b5b;

        font-size: 0.9rem;
    }

    .progress-container {
        margin-top: 1.5rem;
    }

    .progress-header {
        display: flex;

        justify-content: space-between;

        margin-bottom: 0.55rem;

        color: #665b5b;

        font-size: 0.82rem;

        font-weight: 600;
    }

    .progress-track {
        width: 100%;

        height: 9px;

        overflow: hidden;

        border-radius: 999px;

        background: #e4dddd;
    }

    .progress-fill {
        height: 100%;

        border-radius: 999px;

        background: #c4161c;

        animation:
            progressGrow 0.9s ease;
    }


    /* ========================================================
       RISK REASONS
       ======================================================== */

    .reason-card {
        margin-top: 0.6rem;

        padding: 0.9rem 1rem;

        background: #ffffff;

        border-radius: 3px;

        border-left: 4px solid #c4161c;

        color: #4d4444;

        font-size: 0.9rem;

        line-height: 1.5;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.13);
    }


    /* ========================================================
       RECOMMENDATIONS
       ======================================================== */

    .recommendation-card {
        position: relative;

        margin-top: 0.7rem;

        padding: 1rem 1.15rem 1rem 1.25rem;

        background: #ffffff;

        border-radius: 3px;

        border-left: 4px solid #c4161c;

        color: #4d4444;

        font-size: 0.9rem;

        line-height: 1.55;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.13);
    }


    /* ========================================================
       INTERVENTION HISTORY
       ======================================================== */

    .history-card {
        margin-top: 0.65rem;

        padding: 1rem 1.1rem;

        background: #ffffff;

        border-radius: 3px;

        border-left: 4px solid #c4161c;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.13);
    }

    .history-intervention {
        color: #302525;

        font-size: 0.92rem;

        font-weight: 650;

        line-height: 1.45;
    }

    .history-meta {
        margin-top: 0.5rem;

        color: #756969;

        font-size: 0.76rem;
    }

    .history-status {
        display: inline-block;

        margin-top: 0.65rem;

        padding: 0.3rem 0.65rem;

        border-radius: 3px;

        background: #f7e1e1;

        border: 1px solid #e6bfc1;

        color: #a90f15;

        font-size: 0.72rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.05em;
    }

    .history-feedback {
        margin-top: 0.65rem;

        color: #665b5b;

        font-size: 0.82rem;

        line-height: 1.45;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    .custom-divider {
        height: 1px;

        margin: 2rem 0;

        background:
            rgba(
                255,
                255,
                255,
                0.12
            );
    }


    /* ========================================================
       ANIMATION
       ======================================================== */

    @keyframes progressGrow {
        from {
            width: 0;
        }
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .college-header {
            gap: 14px;

            padding: 1rem;
        }

        .college-logo {
            width: 65px;
        }

        .college-name {
            font-size: 1rem;
        }

        .page-header {
            padding: 1.7rem 1.4rem;
        }

        .page-title {
            font-size: 2rem;
        }

        .risk-panel {
            padding: 1.3rem;
        }

        .risk-status {
            font-size: 1.55rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# COLLEGE HEADER
# ============================================================

header_col1, header_col2 = st.columns(
    [1, 15],
    vertical_alignment="center",
)

with header_col1:
    st.image(
        str(LOGO_PATH),
        width=78,
    )

with header_col2:
    st.html(
        """
        <div class="college-name">
            KLE Technological University's, Dr. M. S. Sheshgiri Campus.
        </div>
        """
    )


# ============================================================
# HOME BUTTON
# ============================================================

st.markdown(
    '<div class="home-button-area">',
    unsafe_allow_html=True,
)

if st.button(
    "← Home",
    key="student_home",
):
    st.switch_page("ui/dashboard.py")

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# PAGE HEADER
# ============================================================

st.html(
    """
    <div class="page-header">

        <div class="page-title">
            Student View
        </div>

        <div class="page-subtitle">
            Individual academic performance, risk assessment,
            recommendations and intervention history.
        </div>

    </div>
    """
)


# ============================================================
# STUDENT SEARCH
# ============================================================

st.html(
    """
    <div class="section-title">
        Student Lookup
    </div>

    <div class="section-subtitle">
        Enter a student ID to view the complete student profile.
    </div>
    """
)


student_id = st.text_input(
    "Student ID",
    placeholder="Example: STU003",
    label_visibility="collapsed",
)


if st.button(
    "View Student",
    key="view_student",
):

    normalized_student_id = student_id.strip().upper()

    if not normalized_student_id:

        st.warning(
            "Please enter a Student ID."
        )

    else:

        with st.spinner(
            "Loading student information..."
        ):
            student = get_student(
                normalized_student_id
            )

        if not student:

            st.error(
                f"Student '{normalized_student_id}' was not found."
            )

        else:

            with st.spinner(
                "Analyzing student risk..."
            ):
                risk = analyze_student_risk(
                    normalized_student_id
                )

            if "error" in risk:

                st.error(
                    risk["error"]
                )

            else:

                recommendations = generate_recommendations(
                    student
                )

                intervention_history = (
                    get_intervention_history(
                        normalized_student_id
                    )
                )


                # ====================================================
                # STUDENT DETAILS
                # ====================================================

                st.html(
                    """
                    <div class="custom-divider"></div>

                    <div class="section-title">
                        Student Details
                    </div>

                    <div class="section-subtitle">
                        Basic student identification information.
                    </div>
                    """
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.html(
                        f"""
                        <div class="info-card">

                            <div class="card-label">
                                Student ID
                            </div>

                            <div class="card-value">
                                {html.escape(
                                    str(student["student_id"])
                                )}
                            </div>

                        </div>
                        """
                    )

                with col2:

                    st.html(
                        f"""
                        <div class="info-card">

                            <div class="card-label">
                                Student Name
                            </div>

                            <div class="card-value">
                                {html.escape(
                                    str(student["name"])
                                )}
                            </div>

                        </div>
                        """
                    )


                # ====================================================
                # ACADEMIC PERFORMANCE
                # ====================================================

                st.html(
                    """
                    <div class="section-title">
                        Academic Performance
                    </div>

                    <div class="section-subtitle">
                        Current academic indicators used by
                        the risk system.
                    </div>
                    """
                )

                col1, col2, col3, col4 = st.columns(4)

                academic_values = [
                    (
                        col1,
                        "Attendance",
                        f'{student["attendance"]:.1f}%'
                    ),
                    (
                        col2,
                        "Marks",
                        f'{student["marks"]:.1f}'
                    ),
                    (
                        col3,
                        "Assignments",
                        f'{student["assignments"]:.1f}'
                    ),
                    (
                        col4,
                        "Backlogs",
                        str(student["backlogs"])
                    ),
                ]

                for column, label, value in academic_values:

                    with column:

                        st.html(
                            f"""
                            <div class="academic-card">

                                <div class="academic-label">
                                    {label}
                                </div>

                                <div class="academic-value">
                                    {value}
                                </div>

                            </div>
                            """
                        )


                # ====================================================
                # CAREER STATUS
                # ====================================================

                st.html(
                    """
                    <div class="section-title">
                        Career Status
                    </div>

                    <div class="section-subtitle">
                        Internship and placement readiness information.
                    </div>
                    """
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.html(
                        f"""
                        <div class="status-card">

                            <div class="status-label">
                                Internship Status
                            </div>

                            <div class="status-value">
                                {html.escape(
                                    str(
                                        student[
                                            "internship_status"
                                        ]
                                    )
                                )}
                            </div>

                        </div>
                        """
                    )

                with col2:

                    st.html(
                        f"""
                        <div class="status-card">

                            <div class="status-label">
                                Placement Status
                            </div>

                            <div class="status-value">
                                {html.escape(
                                    str(
                                        student[
                                            "placement_status"
                                        ]
                                    )
                                )}
                            </div>

                        </div>
                        """
                    )


                # ====================================================
                # RISK ASSESSMENT
                # ====================================================

                st.html(
                    """
                    <div class="section-title">
                        Risk Assessment
                    </div>

                    <div class="section-subtitle">
                        Risk classification generated by
                        the student risk analysis agent.
                    </div>
                    """
                )

                probability = float(
                    risk["risk_probability"]
                )

                probability_percent = (
                    probability * 100
                )

                progress_width = max(
                    0,
                    min(
                        probability_percent,
                        100
                    )
                )

                if risk["risk"] == "At Risk":

                    status_class = "risk-danger"

                    status_text = "AT RISK"

                    description = (
                        "The analysis identified indicators "
                        "that require attention."
                    )

                else:

                    status_class = "risk-safe"

                    status_text = "NOT AT RISK"

                    description = (
                        "No significant academic risk indicators "
                        "were detected."
                    )

                st.html(
                    f"""
                    <div class="risk-panel">

                        <div class="risk-status {status_class}">
                            {status_text}
                        </div>

                        <div class="risk-description">
                            {description}
                        </div>

                        <div class="progress-container">

                            <div class="progress-header">

                                <span>
                                    Risk Probability
                                </span>

                                <span>
                                    {probability_percent:.1f}%
                                </span>

                            </div>

                            <div class="progress-track">

                                <div
                                    class="progress-fill"
                                    style="width: {progress_width}%"
                                ></div>

                            </div>

                        </div>

                    </div>
                    """
                )


                # ====================================================
                # RISK REASONS
                # ====================================================

                st.html(
                    """
                    <div class="section-title">
                        Risk Reasons
                    </div>

                    <div class="section-subtitle">
                        Indicators contributing to the student's
                        current assessment.
                    </div>
                    """
                )

                for reason in risk["reasons"]:

                    st.html(
                        f"""
                        <div class="reason-card">
                            {html.escape(str(reason))}
                        </div>
                        """
                    )


                # ====================================================
                # RECOMMENDATIONS
                # ====================================================

                st.html(
                    """
                    <div class="section-title">
                        Recommendations & Action Plan
                    </div>

                    <div class="section-subtitle">
                        Suggested actions based on the student's
                        academic and career indicators.
                    </div>
                    """
                )

                for recommendation in recommendations:

                    st.html(
                        f"""
                        <div class="recommendation-card">
                            {html.escape(
                                str(recommendation)
                            )}
                        </div>
                        """
                    )


                # ====================================================
                # INTERVENTION HISTORY
                # ====================================================

                st.html(
                    """
                    <div class="section-title">
                        Intervention History
                    </div>

                    <div class="section-subtitle">
                        Previously recorded mentor interventions
                        for this student.
                    </div>
                    """
                )

                if not intervention_history:

                    st.info(
                        "No intervention records have been "
                        "created for this student yet."
                    )

                else:

                    for record in reversed(
                        intervention_history
                    ):

                        intervention = html.escape(
                            str(
                                record.get(
                                    "intervention",
                                    "No intervention specified"
                                )
                            )
                        )

                        status = html.escape(
                            str(
                                record.get(
                                    "status",
                                    "unknown"
                                )
                            )
                        )

                        timestamp = html.escape(
                            str(
                                record.get(
                                    "timestamp",
                                    ""
                                )
                            )
                        )

                        feedback = html.escape(
                            str(
                                record.get(
                                    "mentor_feedback",
                                    ""
                                )
                            )
                        )

                        feedback_html = ""

                        if feedback:

                            feedback_html = f"""
                                <div class="history-feedback">
                                    Mentor feedback: {feedback}
                                </div>
                            """

                        st.html(
                            f"""
                            <div class="history-card">

                                <div class="history-intervention">
                                    {intervention}
                                </div>

                                <div class="history-status">
                                    {status}
                                </div>

                                <div class="history-meta">
                                    Recorded: {timestamp}
                                </div>

                                {feedback_html}

                            </div>
                            """
                        )