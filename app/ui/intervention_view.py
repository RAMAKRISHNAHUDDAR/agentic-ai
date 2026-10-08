import html
from pathlib import Path

import streamlit as st

from app.database.database import get_student
from app.memory.intervention_memory import get_intervention_history
from app.safety.approval import (
    approve_intervention,
    reject_intervention,
)


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

        margin-bottom: 1.8rem;
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
       INPUT
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
       TEXT AREA
       ======================================================== */

    div[data-baseweb="textarea"] {
        background: #ffffff;

        border-radius: 3px;

        border: 1px solid #d8d0d0;
    }

    div[data-baseweb="textarea"] textarea {
        color: #302525;
    }

    div[data-baseweb="textarea"]:focus-within {
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
       STUDENT CARD
       ======================================================== */

    .student-card {
        padding: 1.35rem;

        min-height: 105px;

        background: #ffffff;

        border-radius: 4px;

        border-left: 5px solid #c4161c;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.20);
    }

    .student-label {
        color: #756969;

        font-size: 0.72rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }

    .student-value {
        margin-top: 0.55rem;

        color: #302525;

        font-size: 1.4rem;

        font-weight: 700;
    }


    /* ========================================================
       INTERVENTION CARD
       ======================================================== */

    .intervention-card {
        margin-top: 1rem;

        padding: 1.45rem;

        background: #ffffff;

        border-radius: 4px;

        border-top: 4px solid #c4161c;

        box-shadow:
            0 10px 28px rgba(0, 0, 0, 0.20);
    }

    .intervention-label {
        color: #756969;

        font-size: 0.72rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }

    .intervention-text {
        margin-top: 0.6rem;

        color: #302525;

        font-size: 1rem;

        font-weight: 650;

        line-height: 1.55;
    }

    .intervention-time {
        margin-top: 0.65rem;

        color: #756969;

        font-size: 0.76rem;
    }


    /* ========================================================
       STATUS BADGES
       ======================================================== */

    .status-badge {
        display: inline-block;

        margin-top: 0.8rem;

        padding: 0.32rem 0.72rem;

        border-radius: 3px;

        font-size: 0.7rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.06em;
    }

    .status-pending {
        background: #fff4d6;

        border: 1px solid #efd48a;

        color: #946b00;
    }

    .status-approved {
        background: #e2f3e7;

        border: 1px solid #b8dfc2;

        color: #287a45;
    }

    .status-rejected {
        background: #f8e2e2;

        border: 1px solid #e4bcbc;

        color: #b4232d;
    }

    .status-unknown {
        background: #eee9e9;

        border: 1px solid #d8cece;

        color: #665b5b;
    }


    /* ========================================================
       FEEDBACK
       ======================================================== */

    .feedback-box {
        margin-top: 0.9rem;

        padding: 1rem;

        background: #ffffff;

        border-radius: 3px;

        border-left: 4px solid #c4161c;

        color: #4d4444;

        font-size: 0.88rem;

        line-height: 1.55;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.13);
    }

    .feedback-title {
        color: #302525;

        font-weight: 700;

        margin-bottom: 0.35rem;
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

        .intervention-card {
            padding: 1.15rem;
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
    key="intervention_home",
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
            Intervention View
        </div>

        <div class="page-subtitle">
            Mentor review, feedback and intervention approval.
        </div>

    </div>
    """
)


# ============================================================
# STUDENT LOOKUP
# ============================================================

st.html(
    """
    <div class="section-title">
        Student Lookup
    </div>

    <div class="section-subtitle">
        Enter a student ID to review and manage their interventions.
    </div>
    """
)


student_id = st.text_input(
    "Student ID",
    placeholder="Example: STU003",
    label_visibility="collapsed",
)


if st.button(
    "Load Interventions",
    key="load_interventions",
):

    normalized_student_id = (
        student_id.strip().upper()
    )

    if not normalized_student_id:

        st.warning(
            "Please enter a Student ID."
        )

    else:

        student = get_student(
            normalized_student_id
        )

        if not student:

            st.error(
                f"Student '{normalized_student_id}' was not found."
            )

        else:

            st.session_state[
                "intervention_student_id"
            ] = normalized_student_id

            st.rerun()


# ============================================================
# LOAD SELECTED STUDENT
# ============================================================

selected_student_id = st.session_state.get(
    "intervention_student_id"
)


if selected_student_id:

    student = get_student(
        selected_student_id
    )

    if not student:

        st.error(
            f"Student '{selected_student_id}' was not found."
        )

        st.session_state.pop(
            "intervention_student_id",
            None,
        )

    else:

        # ========================================================
        # STUDENT SUMMARY
        # ========================================================

        st.html(
            """
            <div class="custom-divider"></div>

            <div class="section-title">
                Student
            </div>

            <div class="section-subtitle">
                Interventions associated with the selected student.
            </div>
            """
        )

        col1, col2 = st.columns(2)

        with col1:

            st.html(
                f"""
                <div class="student-card">

                    <div class="student-label">
                        Student ID
                    </div>

                    <div class="student-value">
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
                <div class="student-card">

                    <div class="student-label">
                        Student Name
                    </div>

                    <div class="student-value">
                        {html.escape(
                            str(student["name"])
                        )}
                    </div>

                </div>
                """
            )


        # ========================================================
        # INTERVENTION HISTORY
        # ========================================================

        interventions = get_intervention_history(
            selected_student_id
        )

        st.html(
            """
            <div class="section-title">
                Intervention Review
            </div>

            <div class="section-subtitle">
                Review pending interventions and record the
                mentor decision.
            </div>
            """
        )


        if not interventions:

            st.info(
                "No intervention records exist for this student."
            )


        else:

            for index, record in enumerate(
                reversed(interventions)
            ):

                intervention = str(
                    record.get(
                        "intervention",
                        "No intervention specified",
                    )
                )

                status = str(
                    record.get(
                        "status",
                        "unknown",
                    )
                ).lower()

                timestamp = str(
                    record.get(
                        "timestamp",
                        "",
                    )
                )

                feedback = str(
                    record.get(
                        "mentor_feedback",
                        "",
                    )
                )


                # ------------------------------------------------
                # STATUS CLASS
                # ------------------------------------------------

                if status == "pending":

                    status_class = "status-pending"

                elif status == "approved":

                    status_class = "status-approved"

                elif status == "rejected":

                    status_class = "status-rejected"

                else:

                    status_class = "status-unknown"


                # ------------------------------------------------
                # INTERVENTION INFORMATION
                # ------------------------------------------------

                st.html(
                    f"""
                    <div class="intervention-card">

                        <div class="intervention-label">
                            Intervention
                        </div>

                        <div class="intervention-text">
                            {html.escape(intervention)}
                        </div>

                        <div class="status-badge {status_class}">
                            {html.escape(status)}
                        </div>

                        <div class="intervention-time">
                            Recorded: {html.escape(timestamp)}
                        </div>

                    </div>
                    """
                )


                # ------------------------------------------------
                # PENDING INTERVENTION
                # ------------------------------------------------

                if status == "pending":

                    feedback_key = (
                        f"feedback_"
                        f"{selected_student_id}_"
                        f"{index}"
                    )

                    feedback_input = st.text_area(
                        "Mentor Feedback",
                        key=feedback_key,
                        placeholder=(
                            "Enter feedback or instructions "
                            "for this intervention..."
                        ),
                        height=110,
                    )


                    col1, col2 = st.columns(2)


                    with col1:

                        approve_key = (
                            f"approve_"
                            f"{selected_student_id}_"
                            f"{index}"
                        )

                        if st.button(
                            "Approve Intervention",
                            key=approve_key,
                            use_container_width=True,
                        ):

                            result = approve_intervention(
                                selected_student_id,
                                intervention,
                                feedback_input.strip(),
                            )

                            if "error" in result:

                                st.error(
                                    result["error"]
                                )

                            else:

                                st.success(
                                    "Intervention approved successfully."
                                )

                                st.rerun()


                    with col2:

                        reject_key = (
                            f"reject_"
                            f"{selected_student_id}_"
                            f"{index}"
                        )

                        if st.button(
                            "Reject Intervention",
                            key=reject_key,
                            use_container_width=True,
                        ):

                            result = reject_intervention(
                                selected_student_id,
                                intervention,
                                feedback_input.strip(),
                            )

                            if "error" in result:

                                st.error(
                                    result["error"]
                                )

                            else:

                                st.success(
                                    "Intervention rejected successfully."
                                )

                                st.rerun()


                # ------------------------------------------------
                # COMPLETED INTERVENTION
                # ------------------------------------------------

                else:

                    if feedback:

                        st.html(
                            f"""
                            <div class="feedback-box">

                                <div class="feedback-title">
                                    Mentor Feedback
                                </div>

                                {html.escape(feedback)}

                            </div>
                            """
                        )