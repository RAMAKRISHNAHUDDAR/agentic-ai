from pathlib import Path

import streamlit as st


# =========================================================
# PATHS
# =========================================================

LOGO_PATH = (
    Path(__file__).resolve().parent
    / "assets"
    / "kle_tech_logo.png"
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
        background: #2a2020;
        color: #ffffff;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* =====================================================
       COLLEGE HEADER
       ===================================================== */

    .college-header {
        display: flex;
        align-items: center;
        gap: 22px;

        padding: 1.3rem 1.5rem;

        background: #2a2020;

        border-bottom: 3px solid #c4161c;

        margin-bottom: 2.2rem;
    }

    .college-name {
        color: #ffffff;

        font-size: clamp(
            1.15rem,
            2vw,
            1.65rem
        );

        font-weight: 500;

        line-height: 1.4;
    }

    .college-name span {
        display: block;

        margin-top: 2px;

        font-size: 0.95em;

        font-weight: 400;
    }


    /* =====================================================
       WELCOME SECTION
       ===================================================== */

    .welcome-section {
        padding: 2.8rem 2.5rem;

        margin-bottom: 2.2rem;

        background: #c4161c;

        border-radius: 4px;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.25);
    }

    .welcome-label {
        color: #f8dede;

        font-size: 0.85rem;

        font-weight: 600;

        text-transform: uppercase;

        letter-spacing: 0.12em;

        margin-bottom: 0.7rem;
    }

    .welcome-title {
        color: #ffffff;

        font-size: clamp(
            2rem,
            4vw,
            3.2rem
        );

        font-weight: 700;

        line-height: 1.15;

        margin: 0;
    }

    .welcome-description {
        max-width: 850px;

        margin-top: 1rem;

        color: #ffffff;

        font-size: 1rem;

        line-height: 1.7;
    }


    /* =====================================================
       NAVIGATION SECTION
       ===================================================== */

    .section-title {
        color: #ffffff;

        font-size: 1.45rem;

        font-weight: 600;

        margin-bottom: 0.4rem;
    }

    .section-subtitle {
        color: #c8bebe;

        font-size: 0.92rem;

        margin-bottom: 1.5rem;
    }


    /* =====================================================
       NAVIGATION CARDS
       ===================================================== */

    .navigation-card {
        min-height: 260px;

        padding: 2rem;

        background: #ffffff;

        border-radius: 5px;

        border-top: 5px solid #c4161c;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.25);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .navigation-card:hover {
        transform: translateY(-4px);

        box-shadow:
            0 16px 38px rgba(0, 0, 0, 0.32);
    }

    .navigation-card-title {
        color: #302525;

        font-size: 1.45rem;

        font-weight: 700;

        margin-bottom: 0.8rem;
    }

    .navigation-card-description {
        color: #5c5252;

        font-size: 0.92rem;

        line-height: 1.65;

        min-height: 72px;
    }

    .navigation-card-action {
        margin-top: 1.4rem;

        color: #c4161c;

        font-size: 0.85rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }


    /* =====================================================
       INFORMATION SECTION
       ===================================================== */

    .information-panel {
        margin-top: 2.5rem;

        padding: 1.6rem 1.8rem;

        background: #ffffff;

        border-left: 5px solid #c4161c;

        border-radius: 4px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.20);
    }

    .information-title {
        color: #302525;

        font-size: 1.15rem;

        font-weight: 600;

        margin-bottom: 0.55rem;
    }

    .information-text {
        color: #5c5252;

        font-size: 0.9rem;

        line-height: 1.65;

        margin: 0;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        width: 100%;

        min-height: 46px;

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

        transform: translateY(-1px);

        box-shadow:
            0 7px 18px rgba(196, 22, 28, 0.30);
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .page-footer {
        margin-top: 3rem;

        padding-top: 1.2rem;

        border-top:
            1px solid rgba(
                255,
                255,
                255,
                0.12
            );

        text-align: center;

        color: #a99e9e;

        font-size: 0.78rem;
    }


    /* =====================================================
       RESPONSIVE
       ===================================================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .college-header {
            align-items: flex-start;

            gap: 14px;

            padding: 1rem;
        }

        .college-name {
            font-size: 1rem;
        }

        .welcome-section {
            padding: 2rem 1.5rem;
        }

        .welcome-title {
            font-size: 2rem;
        }

        .navigation-card {
            min-height: auto;

            padding: 1.5rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# COLLEGE HEADER
# =========================================================

header_col1, header_col2 = st.columns(
    [1, 15],
    vertical_alignment="center",
)

with header_col1:
    st.image(
        str(LOGO_PATH),
        width=82,
    )

with header_col2:
    st.html(
    """
    <div class="college-name">
        KLE Technological University's, Dr. M. S. Sheshgiri Campus.
    </div>
    """
)


# =========================================================
# WELCOME SECTION
# =========================================================

st.html(
    """
    <div class="welcome-section">

        <div class="welcome-label">
            Student Success & Early Warning System
        </div>

        <div class="welcome-title">
            Welcome
        </div>

        <div class="welcome-description">
            A centralized platform for monitoring student academic
            performance, identifying early risk indicators, and
            supporting timely mentor intervention.
        </div>

    </div>
    """
)


# =========================================================
# NAVIGATION SECTION
# =========================================================

st.html(
    """
    <div class="section-title">
        Application Modules
    </div>

    <div class="section-subtitle">
        Select a module to continue.
    </div>
    """
)


# =========================================================
# NAVIGATION CARDS
# =========================================================

col1, col2 = st.columns(
    2,
    gap="large",
)


with col1:

    st.html(
        """
        <div class="navigation-card">

            <div class="navigation-card-title">
                Student View
            </div>

            <div class="navigation-card-description">
                View student information, academic performance,
                risk assessment, risk indicators, recommendations,
                and intervention history.
            </div>

            <div class="navigation-card-action">
                Student Analysis
            </div>

        </div>
        """
    )

    if st.button(
        "Open Student View",
        key="open_student_view",
    ):
        st.switch_page(
            "ui/student_view.py"
        )


with col2:

    st.html(
        """
        <div class="navigation-card">

            <div class="navigation-card-title">
                Intervention View
            </div>

            <div class="navigation-card-description">
                Review student interventions, provide mentor
                feedback, and approve or reject recommended
                intervention actions.
            </div>

            <div class="navigation-card-action">
                Mentor Intervention
            </div>

        </div>
        """
    )

    if st.button(
        "Open Intervention View",
        key="open_intervention_view",
    ):
        st.switch_page(
            "ui/intervention_view.py"
        )


# =========================================================
# INFORMATION PANEL
# =========================================================

st.html(
    """
    <div class="information-panel">

        <div class="information-title">
            About the System
        </div>

        <p class="information-text">
            The Student Success & Early Warning System helps
            identify students who may require academic support
            and enables mentors to track and manage interventions
            through a centralized workflow.
        </p>

    </div>
    """
)


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div class="page-footer">
        Student Success & Early Warning System
        &nbsp;|&nbsp;
        KLE Technological University
    </div>
    """
)