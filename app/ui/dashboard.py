from app.auth.authentication import login_user, register_user
from pathlib import Path

import streamlit as st


LOGO_PATH = (
    Path(__file__).resolve().parent
    / "assets"
    / "kle_tech_logo.png"
)


# ---------------------------------------------------------
# COLLEGE BRANDING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: #2a2020;
        color: #ffffff;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .college-name {
        color: #ffffff;
        font-size: clamp(1.15rem, 2vw, 1.65rem);
        font-weight: 500;
        line-height: 1.4;
    }

    .login-heading {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-top: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .login-description {
        color: #c8bebe;
        text-align: center;
        margin-bottom: 1.8rem;
    }

    /* White login card with KLE red accent */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border: 1px solid #e0d7d7 !important;
        border-top: 5px solid #c4161c !important;
        border-radius: 5px;
        padding: 1.5rem;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.25);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] h3,
    div[data-testid="stVerticalBlockBorderWrapper"] label {
        color: #302525 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] p,
    div[data-testid="stVerticalBlockBorderWrapper"] small {
        color: #5c5252 !important;
    }

    .stTextInput input {
        border-radius: 3px;
    }

    .stButton > button,
    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        min-height: 46px;
        border-radius: 3px;
        border: 1px solid #c4161c;
        background: #c4161c;
        color: #ffffff;
        font-weight: 600;
    }

    .stButton > button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        background: #a90f15;
        border-color: #a90f15;
        color: #ffffff;
    }

    .demo-credentials {
        color: #c8bebe;
        text-align: center;
        font-size: 0.85rem;
        line-height: 1.8;
        margin-top: 1.2rem;
    }

    .login-footer {
        margin-top: 3rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        text-align: center;
        color: #a99e9e;
        font-size: 0.78rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# COLLEGE HEADER
# ---------------------------------------------------------

header_col1, header_col2 = st.columns(
    [1, 15],
    vertical_alignment="center",
)

with header_col1:
    st.image(str(LOGO_PATH), width=82)

with header_col2:
    st.html(
        """
        <div class="college-name">
            KLE Technological University's,
            Dr. M. S. Sheshgiri Campus.
        </div>
        """
    )

st.markdown(
    "<hr style='border:0;border-top:3px solid #c4161c;'>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# CENTERED LOGIN AND SIGNUP
# ---------------------------------------------------------

st.html(
    """
    <div class="login-heading">Welcome</div>
    <div class="login-description">
        Student Success & Early Warning System
    </div>
    """
)

left, center, right = st.columns([1, 1.15, 1])

with center:
    with st.container(border=True):

        login_tab, signup_tab = st.tabs(["Sign In", "Student Sign Up"])

        # -------------------------------------------------
        # LOGIN
        # -------------------------------------------------

        with login_tab:
            st.markdown("### Sign In")
            st.caption("Sign in using your registered email.")

            with st.form("login_form"):
                email = st.text_input(
                    "Email",
                    placeholder="Enter your registered email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password"
                )

                login_submitted = st.form_submit_button("Sign In")

            if login_submitted:
                try:
                    user = login_user(email, password)

                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_role = user["role"]
                        st.session_state.username = user["email"]
                        st.session_state.user_id = user["user_id"]

                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

                except Exception as error:
                    st.error(f"Login failed: {error}")

        # -------------------------------------------------
        # STUDENT SIGNUP
        # -------------------------------------------------

        with signup_tab:
            st.markdown("### Create Student Account")
            st.caption(
                "Register using your existing student ID."
            )

            with st.form("student_signup_form"):
                student_id = st.text_input(
                    "Student ID",
                    placeholder="Example: STU001"
                )

                signup_email = st.text_input(
                    "Email",
                    placeholder="Enter your email"
                )

                signup_password = st.text_input(
                    "Create Password",
                    type="password",
                    placeholder="Minimum 8 characters"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Re-enter your password"
                )

                signup_submitted = st.form_submit_button(
                    "Create Account"
                )

            if signup_submitted:
                if signup_password != confirm_password:
                    st.error("Passwords do not match.")

                else:
                    try:
                        register_user(
                            user_id=student_id,
                            email=signup_email,
                            password=signup_password,
                            role="student"
                        )

                        st.success(
                            "Account created successfully! "
                            "You can now sign in."
                        )

                    except ValueError as error:
                        st.error(str(error))

                    except Exception:
                        st.error(
                            "Unable to create account. "
                            "Please try again later."
                        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.html(
    """
    <div class="login-footer">
        Student Success & Early Warning System
        &nbsp;|&nbsp;
        KLE Technological University
    </div>
    """
)
