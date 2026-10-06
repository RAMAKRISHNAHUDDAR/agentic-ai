import html

import streamlit as st

from app.database.database import get_student
from app.memory.intervention_memory import get_intervention_history
from app.safety.approval import (
    approve_intervention,
    reject_intervention,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Intervention View | Student Success System",
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

    .intervention-header {
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

    .intervention-header::before {
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
       STUDENT CARD
       ======================================================== */

    .student-card {
        padding: 1.25rem 1.4rem;

        min-height: 105px;

        border-radius: 15px;

        background:
            linear-gradient(
                145deg,
                rgba(30, 41, 59, 0.92),
                rgba(15, 23, 42, 0.88)
            );

        border: 1px solid rgba(148, 163, 184, 0.13);

        box-shadow:
            0 10px 30px rgba(0, 0, 0, 0.20);
    }

    .student-label {
        color: #64748b;

        font-size: 0.72rem;

        font-weight: 650;

        text-transform: uppercase;

        letter-spacing: 0.09em;
    }

    .student-value {
        margin-top: 0.5rem;

        color: #f8fafc;

        font-size: 1.35rem;

        font-weight: 700;
    }


    /* ========================================================
       INTERVENTION CARD
       ======================================================== */

    .intervention-card {
        position: relative;

        margin-top: 1rem;

        padding: 1.45rem;

        border-radius: 17px;

        background:
            linear-gradient(
                145deg,
                rgba(30, 41, 59, 0.94),
                rgba(15, 23, 42, 0.91)
            );

        border: 1px solid rgba(148, 163, 184, 0.14);

        box-shadow:
            0 15px 38px rgba(0, 0, 0, 0.22);

        transition:
            transform 0.22s ease,
            border-color 0.22s ease,
            box-shadow 0.22s ease;
    }

    .intervention-card:hover {
        transform: translateY(-2px);

        border-color:
            rgba(96, 165, 250, 0.30);

        box-shadow:
            0 20px 45px rgba(0, 0, 0, 0.28);
    }

    .intervention-label {
        color: #64748b;

        font-size: 0.72rem;

        font-weight: 650;

        text-transform: uppercase;

        letter-spacing: 0.08em;
    }

    .intervention-text {
        margin-top: 0.6rem;

        color: #e2e8f0;

        font-size: 1rem;

        font-weight: 600;

        line-height: 1.55;
    }

    .intervention-time {
        margin-top: 0.65rem;

        color: #64748b;

        font-size: 0.76rem;
    }


    /* ========================================================
       STATUS BADGES
       ======================================================== */

    .status-badge {
        display: inline-block;

        margin-top: 0.8rem;

        padding: 0.32rem 0.72rem;

        border-radius: 999px;

        font-size: 0.7rem;

        font-weight: 700;

        text-transform: uppercase;

        letter-spacing: 0.06em;
    }

    .status-pending {
        background: rgba(245, 158, 11, 0.10);

        border: 1px solid rgba(245, 158, 11, 0.25);

        color: #fbbf24;
    }

    .status-approved {
        background: rgba(34, 197, 94, 0.10);

        border: 1px solid rgba(34, 197, 94, 0.25);

        color: #4ade80;
    }

    .status-rejected {
        background: rgba(239, 68, 68, 0.10);

        border: 1px solid rgba(239, 68, 68, 0.25);

        color: #f87171;
    }

    .status-unknown {
        background: rgba(148, 163, 184, 0.10);

        border: 1px solid rgba(148, 163, 184, 0.20);

        color: #cbd5e1;
    }


    /* ========================================================
       FEEDBACK
       ======================================================== */

    .feedback-box {
        margin-top: 0.9rem;

        padding: 0.9rem 1rem;

        border-radius: 10px;

        background: rgba(15, 23, 42, 0.75);

        border-left: 3px solid #6366f1;

        color: #cbd5e1;

        font-size: 0.86rem;

        line-height: 1.5;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        min-height: 44px;

        border-radius: 10px;

        font-weight: 650;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
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
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .intervention-header {
            padding: 2.3rem 1.2rem 2rem;
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
# HEADER
# ============================================================

st.html(
    """
    <div class="intervention-header">

        <div class="page-title">
            Intervention View
        </div>

        <div class="header-line"></div>

        <div class="page-subtitle">
            Mentor review, feedback and intervention approval
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


if st.button("Load Interventions"):

    normalized_student_id = student_id.strip().upper()

    if not normalized_student_id:

        st.warning("Please enter a Student ID.")

    else:

        student = get_student(normalized_student_id)

        if not student:

            st.error(
                f"Student '{normalized_student_id}' was not found."
            )

        else:

            # Store the selected student in session state so that
            # approve/reject actions can trigger a clean rerun.
            st.session_state["intervention_student_id"] = (
                normalized_student_id
            )

            st.rerun()


# ============================================================
# LOAD SELECTED STUDENT
# ============================================================

selected_student_id = st.session_state.get(
    "intervention_student_id"
)


if selected_student_id:

    student = get_student(selected_student_id)

    if not student:

        st.error(
            f"Student '{selected_student_id}' was not found."
        )

        st.session_state.pop(
            "intervention_student_id",
            None
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
                        {html.escape(str(student["student_id"]))}
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
                        {html.escape(str(student["name"]))}
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
                Review pending interventions and record the mentor decision.
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
                        "No intervention specified"
                    )
                )

                status = str(
                    record.get(
                        "status",
                        "unknown"
                    )
                ).lower()

                timestamp = str(
                    record.get(
                        "timestamp",
                        ""
                    )
                )

                feedback = str(
                    record.get(
                        "mentor_feedback",
                        ""
                    )
                )

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
                        f"feedback_{selected_student_id}_{index}"
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
                            f"approve_{selected_student_id}_{index}"
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
                            f"reject_{selected_student_id}_{index}"
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

                                <strong>Mentor Feedback</strong><br>

                                {html.escape(feedback)}

                            </div>
                            """
                        )