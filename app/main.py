import streamlit as st

st.set_page_config(
    page_title="Student Success & Early Warning System",
    page_icon="🎓",
    layout="wide",
)

dashboard = st.Page(
    "ui/dashboard.py",
    title="Dashboard",
    icon="📊",
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

pg = st.navigation(
    [
        dashboard,
        student_view,
        intervention_view,
    ],
    position="hidden",
)

pg.run()