import streamlit as st

from app.workflows.node_graph import StudentSuccessNodeGraph


st.set_page_config(
    page_title="Student Success & Early Warning System",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Student Success & Early Warning System")
st.write("Student Risk Dashboard")

st.divider()

st.subheader("Student Search")

student_id = st.text_input(
    "Enter Student ID",
    placeholder="Example: STU003",
)

if st.button("Analyze Student"):

    if not student_id:
        st.warning("Please enter a Student ID.")

    else:
        with st.spinner("Analyzing student..."):

            workflow = StudentSuccessNodeGraph()
            result = workflow.run(student_id.strip().upper())

        if result["status"] == "error":

            st.error(result["message"])

        else:

            student = result["student"]
            risk = result["risk"]

            st.success("Student analysis completed.")

            st.divider()

            st.subheader("Student Information")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Student ID",
                    student["student_id"]
                )

            with col2:
                st.metric(
                    "Name",
                    student["name"]
                )

            st.divider()

            st.subheader("Academic Information")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Attendance",
                    f"{student['attendance']}%"
                )

            with col2:
                st.metric(
                    "Marks",
                    student["marks"]
                )

            with col3:
                st.metric(
                    "Assignments",
                    student["assignments"]
                )

            with col4:
                st.metric(
                    "Backlogs",
                    student["backlogs"]
                )

            st.divider()

            st.subheader("⚠️ Risk Analysis")

            if risk["risk"] == "At Risk":
                st.error("🔴 AT RISK")
            else:
                st.success("🟢 NOT AT RISK")

            st.metric(
                "Risk Probability",
                f"{risk['risk_probability']:.2%}"
            )

            st.write("**Reasons:**")

            for reason in risk["reasons"]:
                st.write(f"- {reason}")