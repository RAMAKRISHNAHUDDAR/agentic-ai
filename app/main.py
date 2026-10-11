
import streamlit as st

st.set_page_config(
    page_title="Student Success & Early Warning System",
    page_icon="🎓",
    layout="wide",
)

# Demo credentials
DEMO_USERS = {
    "mentor": {
        "password": "mentor123",
        "role": "mentor",
    },
    "student": {
        "password": "student123",
        "role": "student",
    },
}

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

# Register pages
login_page = st.Page(
    "ui/dashboard.py",
    title="Login",
    icon="🔐",
)

student_view = st.Page(
    "ui/student_view.py",
    title="Student View",
    icon="👨‍🎓",
)

intervention_view = st.Page(
    "ui/intervention_view.py",
    title="Intervention View",
    icon="🛡️",
)

# Show login until a user signs in
if not st.session_state.logged_in:
    pg = st.navigation([login_page], position="hidden")

elif st.session_state.user_role == "mentor":
    pg = st.navigation([intervention_view], position="hidden")

elif st.session_state.user_role == "student":
    pg = st.navigation([student_view], position="hidden")

else:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.rerun()

pg.run()
