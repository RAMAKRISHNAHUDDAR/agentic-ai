
import streamlit as st


def is_authenticated():
    """Check whether a user is logged in."""

    return (
        st.session_state.get("logged_in", False)
        and st.session_state.get("user_role") in {"student", "mentor"}
    )


def require_login():
    """Prevent access to pages without authentication."""

    if not is_authenticated():
        st.error("Please log in to access this page.")
        st.stop()


def require_role(required_role):
    """Allow access only to users with the required role."""

    require_login()

    if st.session_state.get("user_role") != required_role:
        st.error("You do not have permission to access this page.")
        st.stop()
