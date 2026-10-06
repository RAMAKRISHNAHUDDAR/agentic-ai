from app.agents.risk_agent import analyze_student_risk


def risk_analysis_skill(student_id):
    """
    Reusable skill for analyzing a student's academic risk.

    Args:
        student_id: Student ID to analyze.

    Returns:
        Dictionary containing the student's risk analysis.
    """
    if not student_id:
        return {"error": "Student ID is required"}

    return analyze_student_risk(student_id)


if __name__ == "__main__":
    student_id = input("Enter student ID: ")

    result = risk_analysis_skill(student_id)

    print("\nRisk Analysis Skill")
    print("-------------------")

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Student ID: {result['student_id']}")
        print(f"Name: {result['name']}")
        print(f"Risk: {result['risk']}")
        print(f"Risk Probability: {result['risk_probability']:.2%}")

        print("\nReasons:")
        for reason in result["reasons"]:
            print(f"- {reason}")