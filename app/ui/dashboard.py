import streamlit as st

from app.workflows.node_graph import StudentSuccessNodeGraph


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Student Success & Early Warning System",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(37, 99, 235, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(124, 58, 237, 0.10),
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


    /* =====================================================
       PREMIUM HEADER
       ===================================================== */

    .dashboard-header {
        position: relative;

        padding: 3.2rem 2rem 2.8rem;

        margin-bottom: 2.5rem;

        border-radius: 24px;

        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(59, 130, 246, 0.16),
                transparent 42%
            ),
            linear-gradient(
                145deg,
                rgba(25, 38, 62, 0.98),
                rgba(11, 18, 32, 0.96)
            );

        border: 1px solid rgba(148, 163, 184, 0.16);

        box-shadow:
            0 25px 70px rgba(0, 0, 0, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);

        text-align: center;

        overflow: hidden;
    }


    /* Top glowing accent */

    .dashboard-header::before {
        content: "";

        position: absolute;

        top: 0;
        left: 50%;

        width: 420px;
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
            0 0 25px rgba(96, 165, 250, 0.6);
    }


    /* Main heading */

    .dashboard-title {
        position: relative;

        margin: 0 auto;

        font-size: clamp(2rem, 4vw, 3.2rem);

        font-weight: 800;

        line-height: 1.15;

        letter-spacing: -0.045em;

        background:
            linear-gradient(
                90deg,
                #ffffff 10%,
                #dbeafe 45%,
                #93c5fd 70%,
                #ffffff 95%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    /* Accent line under heading */

    .dashboard-title::after {
        content: "";

        display: block;

        width: 70px;
        height: 3px;

        margin: 1.15rem auto 0;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                #3b82f6,
                #8b5cf6
            );

        box-shadow:
            0 0 15px rgba(99, 102, 241, 0.45);
    }


    /* Subtitle */

    .dashboard-subtitle {
        margin-top: 1.25rem;

        color: #94a3b8;

        font-size: 0.98rem;

        font-weight: 400;

        letter-spacing: 0.02em;
    }


    /* System status */

    .status-line {
        display: inline-flex;

        align-items: center;
        justify-content: center;

        gap: 9px;

        margin-top: 1.5rem;

        padding: 0.48rem 1rem;

        border-radius: 999px;

        background: rgba(34, 197, 94, 0.07);

        border: 1px solid rgba(34, 197, 94, 0.18);

        color: #86efac;

        font-size: 0.78rem;

        font-weight: 600;

        letter-spacing: 0.03em;
    }


    /* Status indicator */

    .status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #22c55e;

        box-shadow:
            0 0 8px rgba(34, 197, 94, 0.8),
            0 0 18px rgba(34, 197, 94, 0.4);
    }


    /* =====================================================
       SECTION HEADERS
       ===================================================== */

    .section-title {
        margin-top: 2rem;

        margin-bottom: 0.55rem;

        font-size: 1.3rem;

        font-weight: 700;

        color: #f8fafc;
    }

    .section-subtitle {
        margin-bottom: 1.3rem;

        color: #64748b;

        font-size: 0.9rem;
    }


    /* =====================================================
       SEARCH AREA
       ===================================================== */

    div[data-baseweb="input"] {
        background: rgba(15, 23, 42, 0.85);

        border-radius: 10px;

        border: 1px solid rgba(148, 163, 184, 0.18);
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #3b82f6;

        box-shadow:
            0 0 0 1px rgba(59, 130, 246, 0.35),
            0 0 20px rgba(59, 130, 246, 0.08);
    }


    /* Search button */

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

        font-weight: 600;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 10px 28px rgba(37, 99, 235, 0.32);
    }


    /* =====================================================
       STUDENT INFORMATION CARDS
       ===================================================== */

    .info-card {
        padding: 1.4rem;

        min-height: 110px;

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
        transform: translateY(-4px);

        border-color:
            rgba(96, 165, 250, 0.35);

        box-shadow:
            0 18px 40px rgba(0, 0, 0, 0.30);
    }

    .card-label {
        color: #64748b;

        font-size: 0.76rem;

        font-weight: 650;

        text-transform: uppercase;

        letter-spacing: 0.09em;
    }

    .card-value {
        margin-top: 0.55rem;

        color: #f8fafc;

        font-size: 1.5rem;

        font-weight: 700;
    }


    /* =====================================================
       ACADEMIC CARDS
       ===================================================== */

    .academic-card {
        padding: 1.25rem;

        min-height: 115px;

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
        transform: translateY(-4px);

        border-color:
            rgba(59, 130, 246, 0.38);

        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.25);
    }

    .academic-label {
        color: #64748b;

        font-size: 0.75rem;

        font-weight: 650;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }

    .academic-value {
        margin-top: 0.45rem;

        color: #f8fafc;

        font-size: 1.75rem;

        font-weight: 750;
    }


    /* =====================================================
       RISK PANEL
       ===================================================== */

    .risk-panel {
        margin-top: 0.8rem;

        padding: 2rem;

        border-radius: 20px;

        background:
            linear-gradient(
                145deg,
                rgba(30, 41, 59, 0.96),
                rgba(15, 23, 42, 0.92)
            );

        border: 1px solid rgba(148, 163, 184, 0.14);

        box-shadow:
            0 20px 50px rgba(0, 0, 0, 0.25);
    }

    .risk-status {
        font-size: 2rem;

        font-weight: 800;

        letter-spacing: -0.025em;
    }

    .risk-status-danger {
        color: #f87171;
    }

    .risk-status-safe {
        color: #4ade80;
    }

    .risk-description {
        margin-top: 0.55rem;

        color: #94a3b8;

        font-size: 0.92rem;
    }


    /* =====================================================
       RISK PROGRESS
       ===================================================== */

    .progress-container {
        margin-top: 1.7rem;
    }

    .progress-header {
        display: flex;

        justify-content: space-between;

        margin-bottom: 0.6rem;

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
            progressGrow 1s ease;
    }


    /* =====================================================
       RISK INDICATORS
       ===================================================== */

    .reason-card {
        margin-top: 0.65rem;

        padding: 0.95rem 1rem;

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


    /* =====================================================
       DIVIDER
       ===================================================== */

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


    /* =====================================================
       STREAMLIT ALERTS
       ===================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* =====================================================
       ANIMATIONS
       ===================================================== */

    @keyframes fadeIn {

        from {
            opacity: 0;

            transform:
                translateY(10px);
        }

        to {
            opacity: 1;

            transform:
                translateY(0);
        }
    }

    @keyframes progressGrow {

        from {
            width: 0;
        }
    }


    /* =====================================================
       RESPONSIVE DESIGN
       ===================================================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .dashboard-header {
            padding:
                2.5rem 1.2rem 2.2rem;
        }

        .dashboard-title {
            font-size: 2rem;
        }

        .dashboard-subtitle {
            font-size: 0.9rem;
        }

        .risk-panel {
            padding: 1.4rem;
        }

        .risk-status {
            font-size: 1.6rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.html(
    """
    <div class="dashboard-header">

        <div class="dashboard-title">
            Student Success & Early Warning System
        </div>

        <div class="dashboard-subtitle">
            Academic performance monitoring and early risk identification
        </div>

        <div class="status-line">
            <span class="status-dot"></span>
            <span>System operational</span>
        </div>

    </div>
    """
)


# =========================================================
# STUDENT SEARCH
# =========================================================

st.html(
    """
    <div class="section-title">
        Student Search
    </div>

    <div class="section-subtitle">
        Enter a student ID to generate an academic risk assessment.
    </div>
    """
)


student_id = st.text_input(
    "Student ID",
    placeholder="Example: STU003",
    label_visibility="collapsed",
)


if st.button("Analyze Student"):

    # =====================================================
    # VALIDATE INPUT
    # =====================================================

    if not student_id:

        st.warning(
            "Please enter a Student ID."
        )

    else:

        # =================================================
        # RUN WORKFLOW
        # =================================================

        with st.spinner(
            "Analyzing student data..."
        ):

            workflow = StudentSuccessNodeGraph()

            result = workflow.run(
                student_id.strip().upper()
            )


        # =================================================
        # HANDLE ERROR
        # =================================================

        if result["status"] == "error":

            st.error(
                result["message"]
            )


        # =================================================
        # DISPLAY RESULT
        # =================================================

        else:

            student = result["student"]

            risk = result["risk"]


            st.success(
                "Student analysis completed."
            )


            # =================================================
            # STUDENT INFORMATION
            # =================================================

            st.html(
                """
                <div class="custom-divider"></div>

                <div class="section-title">
                    Student Information
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
                            {student["student_id"]}
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
                            {student["name"]}
                        </div>

                    </div>
                    """
                )


            # =================================================
            # ACADEMIC PERFORMANCE
            # =================================================

            st.html(
                """
                <div class="section-title">
                    Academic Performance
                </div>
                """
            )


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.html(
                    f"""
                    <div class="academic-card">

                        <div class="academic-label">
                            Attendance
                        </div>

                        <div class="academic-value">
                            {student["attendance"]}%
                        </div>

                    </div>
                    """
                )


            with col2:

                st.html(
                    f"""
                    <div class="academic-card">

                        <div class="academic-label">
                            Marks
                        </div>

                        <div class="academic-value">
                            {student["marks"]}
                        </div>

                    </div>
                    """
                )


            with col3:

                st.html(
                    f"""
                    <div class="academic-card">

                        <div class="academic-label">
                            Assignments
                        </div>

                        <div class="academic-value">
                            {student["assignments"]}
                        </div>

                    </div>
                    """
                )


            with col4:

                st.html(
                    f"""
                    <div class="academic-card">

                        <div class="academic-label">
                            Backlogs
                        </div>

                        <div class="academic-value">
                            {student["backlogs"]}
                        </div>

                    </div>
                    """
                )


            # =================================================
            # RISK ASSESSMENT
            # =================================================

            st.html(
                """
                <div class="section-title">
                    Risk Assessment
                </div>
                """
            )


            probability = risk["risk_probability"]

            probability_percent = (
                probability * 100
            )


            if risk["risk"] == "At Risk":

                status_class = (
                    "risk-status-danger"
                )

                status_text = "AT RISK"

                description = (
                    "The analysis identified indicators "
                    "that require attention."
                )

            else:

                status_class = (
                    "risk-status-safe"
                )

                status_text = "NOT AT RISK"

                description = (
                    "No significant academic risk indicators "
                    "were detected."
                )


            # Keep progress width between 0 and 100

            progress_width = max(
                0,
                min(
                    probability_percent,
                    100
                )
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


            # =================================================
            # RISK INDICATORS
            # =================================================

            st.html(
                """
                <div class="section-title">
                    Risk Indicators
                </div>
                """
            )


            for reason in risk["reasons"]:

                st.html(
                    f"""
                    <div class="reason-card">
                        {reason}
                    </div>
                    """
                )