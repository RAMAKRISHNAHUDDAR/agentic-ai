
import re


# Allowed values
USER_ROLES = {"student", "mentor"}

INTERVENTION_STATUSES = {
    "pending",
    "approved",
    "rejected"
}

NOTIFICATION_STATUSES = {
    "pending",
    "sent",
    "failed"
}


def validate_required_fields(data, fields):
    """Check whether all required fields are present and non-empty."""

    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary.")

    for field in fields:
        value = data.get(field)

        if value is None or (
            isinstance(value, str) and not value.strip()
        ):
            raise ValueError(
                f"Required field is missing: {field}"
            )

    return True


def validate_email(email):
    """Validate email address format."""

    if not isinstance(email, str):
        raise ValueError("Email must be a string.")

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(pattern, email):
        raise ValueError("Invalid email address.")

    return True


def validate_boolean(value, field):
    """Check whether a value is a boolean."""

    if not isinstance(value, bool):
        raise ValueError(f"{field} must be True or False.")

    return True


def validate_percentage(value, field):
    """Validate percentage values between 0 and 100."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be a number.")

    if not 0 <= value <= 100:
        raise ValueError(
            f"{field} must be between 0 and 100."
        )

    return True


def validate_user(data):
    """Validate user account information."""

    validate_required_fields(
        data,
        ["user_id", "email", "password_hash", "role"]
    )

    validate_email(data["email"])

    if data["role"] not in USER_ROLES:
        raise ValueError("Role must be student or mentor.")

    if "is_active" in data:
        validate_boolean(data["is_active"], "is_active")

    return True


def validate_student(data):
    """Validate student information."""

    validate_required_fields(
        data,
        [
            "student_id",
            "name",
            "attendance",
            "marks",
            "assignments",
            "backlogs",
            "internship_status",
            "placement_status",
            "risk_label"
        ]
    )

    validate_percentage(data["attendance"], "attendance")
    validate_percentage(data["marks"], "marks")
    validate_percentage(data["assignments"], "assignments")

    backlogs = data["backlogs"]

    if isinstance(backlogs, bool) or not isinstance(backlogs, int):
        raise ValueError("Backlogs must be an integer.")

    if backlogs < 0:
        raise ValueError("Backlogs cannot be negative.")

    if data.get("parent_id") is not None:
        if not isinstance(data["parent_id"], str) or not data["parent_id"].strip():
            raise ValueError("Invalid parent_id.")

    return True


def validate_parent(data):
    """Validate parent information."""

    validate_required_fields(
        data,
        ["parent_id", "name", "phone", "email"]
    )

    validate_email(data["email"])

    if "email_opt_in" in data:
        validate_boolean(
            data["email_opt_in"],
            "email_opt_in"
        )

    return True


def validate_mentor(data):
    """Validate mentor information."""

    validate_required_fields(
        data,
        ["mentor_id", "name", "email", "department"]
    )

    validate_email(data["email"])

    if "is_active" in data:
        validate_boolean(data["is_active"], "is_active")

    return True


def validate_intervention(data):
    """Validate intervention information."""

    validate_required_fields(
        data,
        [
            "intervention_id",
            "student_id",
            "description",
            "status"
        ]
    )

    if data["status"] not in INTERVENTION_STATUSES:
        raise ValueError(
            "Intervention status must be pending, approved or rejected."
        )

    return True


def validate_notification(data):
    """Validate email notification information."""

    validate_required_fields(
        data,
        [
            "notification_id",
            "intervention_id",
            "student_id",
            "parent_id",
            "recipient_email",
            "notification_type",
            "status"
        ]
    )

    validate_email(data["recipient_email"])

    if data["notification_type"] != "email":
        raise ValueError(
            "Notification type must be email."
        )

    if data["status"] not in NOTIFICATION_STATUSES:
        raise ValueError(
            "Notification status must be pending, sent or failed."
        )

    return True


def validate_parent_reference(db, parent_id):
    """Check whether the parent exists in MongoDB."""

    if not parent_id:
        return True

    parent = db.parents.find_one(
        {"parent_id": parent_id}
    )

    if not parent:
        raise ValueError(
            f"Parent does not exist: {parent_id}"
        )

    return True


def validate_student_reference(db, student_id):
    """Check whether the student exists in MongoDB."""

    student = db.students.find_one(
        {"student_id": student_id}
    )

    if not student:
        raise ValueError(
            f"Student does not exist: {student_id}"
        )

    return True
