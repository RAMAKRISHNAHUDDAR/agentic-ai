import html

import streamlit as st

from app.database.database import get_student
from app.agents.risk_agent import analyze_student_risk
from app.agents.recommendation_agent import generate_recommendations
from app.memory.intervention_memory import get_intervention_history


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Student View | Student Success System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
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
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(37, 99, 235, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(124, 58, 237, 0.08),
                transparent 30%
            ),
            #080b12;

        color: #f5f7fb;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .student-header {
        position: relative;

        padding: 2.8rem 2rem 2.5rem;
        margin-bottom: 2rem;

        border-radius: 24px;

        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(59, 130, 246, 0.15),
                transparent 45%
            ),
            linear-gradient(
                145deg,
                rgba(25, 38, 62, 0.98),
                rgba(11, 18, 32, 0.96)
            );

        border: 1px solid rgba(148, 163, 184, 0.16);

        box-shadow:
            0 25px 70px rgba(0, 0, 0, 0.32),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);

        text-align: center;

        overflow: hidden;
    }

    .student-header::before {
        content: "";

        position: absolute;

        top: 0;
        left: 50%;

        width: 380px;
        height: 2px;

        transform: translateX(-50%);

        background:
            linear-gradient(
                90deg,
                transparent,
                #60a5fa,
                #818cf8,
                transparent
            );

        box-shadow:
            0 0 25px rgba(96, 165, 250, 0.55);
    }

    .page-title {
        margin: 0;

        font-size: clamp(2rem, 4vw, 3rem);

        font-weight: 800;

        line-height: 1.15;

        letter-spacing: -0.045em;

        background:
            linear-gradient(
                90deg,
                #ffffff 10%,
                #dbeafe 50%,
                #93c5fd 75%,
                #ffffff 95%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .page-subtitle {
        margin-top: 1rem;

        color: #94a3b8;

        font-size: 0.95rem;

        letter-spacing: 0.02em;
    }

    .header-line {
        width: 65px;
        height: 3px;

        margin: 1.1rem auto 0;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                #3b82f6,
                #8b5cf6
            );

        box-shadow:
            0 0 15px rgba(99, 102, 241, 0.4);
    }


    /* ========================================================
       SECTION HEADERS
       ======================================================== */

    .section-title {
        margin-top: 2rem;
        margin-bottom: 0.45rem;

        color: #f8fafc;

        font-size: 1.25rem;
        font-weight: 750;

        letter-spacing: -0.015em;
    }

    .section-subtitle {
        margin-bottom: 1.15rem;

        color: #64748b;

        font-size: 0.88rem;
    }


    /* ========================================================
       SEARCH
       ======================================================== */

    div[data-baseweb="input"] {
        background: rgba(15, 23, 42, 0.88);

        border-radius: 11px;

        border: 1px solid rgba(148, 163, 184, 0.18);
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #3b82f6;

        box-shadow:
            0 0 0 1px rgba(59, 130, 246, 0.3),
            0 0 20px rgba(59, 130, 246, 0.08);
    }

    .stButton > button {
        min-height: 44px;

        border-radius: 10px;

        border: 1px solid rgba(96, 165, 250, 0.35);

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #4f46e5
            );

        color: white;

        font-weight: 650;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 10px 28px rgba(37, 99, 235, 0.32);
    }


    /* ========================================================
       INFORMATION CARDS
       ======================================================== */

    .info-card {
        padding: 1.35rem;

        min-height: 108px;

        border-radius: 16px;

        background:
            linear-gradient(
                145deg,
                rgba(30, 41, 59, 0.92),
                rgba(15, 23, 42, 0.88)
            );

        border: 1px solid rgba(148, 163, 184, 0.13);

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.20);

        transition:
            transform 0.25s ease,
            border-color 0.25s ease,
            box-shadow 0.25s ease;
    }

    .info-card:hover {
        transform: translateY(-3px);

        border-color:
            rgba(96, 165, 250, 0.35);

        box-shadow:
            0 18px 40px rgba(0, 0, 0, 0.28);
    }

    .card-label {
        color: #64748b;

        font-size: 0.72rem;

        font-weight: 650;

        text-transform: uppercase;

        letter-spacing: 0.09em;
    }

    .card-value {
        margin-top: 0.55rem;

        color: #f8fafc;

        font-size: 1.45rem;

        font-weight: 700;
    }


    /* ========================================================
       ACADEMIC CARDS
       ======================================================== */

    .academic-card {
        padding: 1.25rem;

        min-height: 112px;

        border-radius: 15px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.94),
                rgba(17, 24, 39, 0.90)
            );

        border: 1px solid rgba(148, 163, 184, 0.13);

        transition:
            transform 0.25s ease,
            border-color 0.25s ease,
            box-shadow 0.25s ease;
    }

    .academic-card:hover {
        transform: translateY(-3px);

        border-color:
            rgba(59, 130, 246, 0.38);

        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.25);
    }

    .academic-label {
        color: #64748b;

        font-size: 0.72rem;

        font-weight: 650;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }

    .academic-value {
        margin-top: 0.45rem;

        color: #f8fafc;

        font-size: 1.65rem;

        font-weight: 750;
    }


    /* ========================================================
       STATUS CARD
       ======================================================== */

    .status-card {
        padding: 1.25rem;

        min-height: 112px;

        border-radius: 15px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.94),
                rgba(17, 24, 39, 0.90)
            );

        border: 1px solid rgba(148, 163, 184, 0.13);

        transition:
            transform 0.25s ease,
            border-color 0.25s ease;
    }

    .status-card:hover {
        transform: translateY(-3px);

        border-color:
            rgba(96, 165, 250, 0.32);
    }

    .status-label {
        color: #64748b;

        font-size: 0.72rem;

        font-weight: 650;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }

    .status-value {
        margin-top: 0.55rem;

        color: #e2e8f0;

        font-size: 1rem;

        font-weight: 650;
    }


    /* ========================================================
       RISK PANEL
       ======================================================== */

    .risk-panel {
        margin-top: 0.5rem;

        padding: 1.8rem;

        border-radius: 20px;

        background:
            linear-gradient(
                145deg,
                rgba(30, 41, 59, 0.96),
                rgba(15, 23, 42, 0.92)
            );

        border: 1px solid rgba(148, 163, 184, 0.14);

        box-shadow:
            0 20px 50px rgba(0, 0, 0, 0.24);
    }

    .risk-status {
        font-size: 1.9rem;

        font-weight: 800;

        letter-spacing: -0.025em;
    }

    .risk-danger {
        color: #f87171;
    }

    .risk-safe {
        color: #4ade80;
    }

    .risk-description {
        margin-top: 0.45rem;

        color: #94a3b8;

        font-size: 0.9rem;
    }

    .progress-container {
        margin-top: 1.5rem;
    }

    .progress-header {
        display: flex;

        justify-content: space-between;

        margin-bottom: 0.55rem;

        color: #94a3b8;

        font-size: 0.82rem;
    }

    .progress-track {
        width: 100%;

        height: 9px;

        overflow: hidden;

        border-radius: 999px;

        background: #1e293b;
    }

    .progress-fill {
        height: 100%;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                #3b82f6,
                #8b5cf6
            );

        box-shadow:
            0 0 14px rgba(99, 102, 241, 0.35);

        animation:
            progressGrow 0.9s ease;
    }


    /* ========================================================
       RISK REASONS
       ======================================================== */

    .reason-card {
        margin-top: 0.6rem;

        padding: 0.9rem 1rem;

        border-radius: 10px;

        background:
            rgba(30, 41, 59, 0.65);

        border-left:
            3px solid #3b82f6;

        color: #cbd5e1;

        font-size: 0.9rem;

        transition:
            background 0.2s ease,
            transform 0.2s ease;
    }

    .reason-card:hover {
        background:
            rgba(30, 41, 59, 0.90);

        transform:
            translateX(3px);
    }


    /* ========================================================
       RECOMMENDATION CARDS
       ======================================================== */

    .recommendation-card {
        position: relative;

        margin-top: 0.7rem;

        padding: 1rem 1.15rem 1rem 1.25rem;

        border-radius: 12px;

        background:
            linear-gradient(
                145deg,
                rgba(30, 41, 59, 0.82),
                rgba(15, 23, 42, 0.78)
            );

        border: 1px solid rgba(148, 163, 184, 0.13);

        color: #dbe4f0;

        font-size: 0.9rem;

        line-height: 1.5;

        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            background 0.2s ease;
    }

    .recommendation-card::before {
        content: "";

        position: absolute;

        left: 0;
        top: 12px;
        bottom: 12px;

        width: 3px;

        border-radius: 999px;

        background:
            linear-gradient(
                180deg,
                #3b82f6,
                #8b5cf6
            );
    }

    .recommendation-card:hover {
        transform: translateX(3px);

        border-color:
            rgba(96, 165, 250, 0.30);

        background:
            rgba(30, 41, 59, 0.94);
    }


    /* ========================================================
       INTERVENTION HISTORY
       ======================================================== */

    .history-card {
        margin-top: 0.65rem;

        padding: 1rem 1.1rem;

        border-radius: 12px;

        background:
            rgba(15, 23, 42, 0.82);

        border: 1px solid rgba(148, 163, 184, 0.12);
    }

    .history-intervention {
        color: #e2e8f0;

        font-size: 0.92rem;

        font-weight: 600;

        line-height: 1.45;
    }

    .history-meta {
        margin-top: 0.5rem;

        color: #64748b;

        font-size: 0.76rem;
    }

    .history-status {
        display: inline-block;

        margin-top: 0.65rem;

        padding: 0.3rem 0.65rem;

        border-radius: 999px;

        background: rgba(59, 130, 246, 0.10);

        border: 1px solid rgba(59, 130, 246, 0.20);

        color: #93c5fd;

        font-size: 0.72rem;

        font-weight: 650;

        text-transform: uppercase;

        letter-spacing: 0.05em;
    }

    .history-feedback {
        margin-top: 0.65rem;

        color: #94a3b8;

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
            linear-gradient(
                90deg,
                transparent,
                rgba(148, 163, 184, 0.20),
                transparent
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

        .student-header {
            padding: 2.3rem 1.2rem 2rem;
        }

        .page-title {
            font-size: 2rem;
        }

        .risk-panel {
            padding: 1.35rem;
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
# HEADER
# ============================================================

st.html(
    """
    <div class="student-header">

        <div class="page-title">
            Student View
        </div>

        <div class="header-line"></div>

        <div class="page-subtitle">
            Individual academic performance, risk assessment and action plan
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


if st.button("View Student"):

    normalized_student_id = student_id.strip().upper()

    if not normalized_student_id:

        st.warning("Please enter a Student ID.")

    else:

        with st.spinner("Loading student information..."):

            student = get_student(normalized_student_id)

        if not student:

            st.error(
                f"Student '{normalized_student_id}' was not found."
            )

        else:

            with st.spinner("Analyzing student risk..."):

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

                intervention_history = get_intervention_history(
                    normalized_student_id
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
                                {html.escape(str(student["student_id"]))}
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
                                {html.escape(str(student["name"]))}
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
                        Current academic indicators used by the risk system.
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
                                {html.escape(str(student["internship_status"]))}
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
                                {html.escape(str(student["placement_status"]))}
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
                        Risk classification generated by the student risk analysis agent.
                    </div>
                    """
                )

                probability = float(
                    risk["risk_probability"]
                )

                probability_percent = probability * 100

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
                        Indicators contributing to the student's current assessment.
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
                        Suggested actions based on the student's academic and career indicators.
                    </div>
                    """
                )

                for recommendation in recommendations:

                    st.html(
                        f"""
                        <div class="recommendation-card">
                            {html.escape(str(recommendation))}
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
                        Previously recorded mentor interventions for this student.
                    </div>
                    """
                )

                if not intervention_history:

                    st.info(
                        "No intervention records have been created for this student yet."
                    )

                else:

                    for record in reversed(intervention_history):

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