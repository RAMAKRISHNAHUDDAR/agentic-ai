from mcp.server import MCPServer

from app.database.database import get_student, get_all_students


server = MCPServer("student-success-server")


@server.tool()
def get_student_from_database(student_id: str) -> dict:
    """Get student information from SQLite database."""
    student = get_student(student_id)

    if not student:
        return {"error": "Student not found"}

    return student


@server.tool()
def get_all_students_from_database() -> list:
    """Get all students from SQLite database."""
    return get_all_students()


@server.resource("file://students")
def get_student_file() -> str:
    """Provide the student CSV file as a resource."""
    with open("data/students.csv", "r", encoding="utf-8") as file:
        return file.read()


@server.tool()
def get_student_api_data(student_id: str) -> dict:
    """Mock API returning student data."""
    student = get_student(student_id)

    if not student:
        return {"error": "Student not found"}

    return {
        "source": "mock_api",
        "student_id": student_id,
        "status": "success",
        "data": student,
    }


if __name__ == "__main__":
    server.run()