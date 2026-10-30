
from datetime import datetime, timezone

from bson import ObjectId
from pymongo.errors import DuplicateKeyError, PyMongoError

from app.database.mongodb import get_database
from app.database import validators


# --------------------------------------------------
# COMMON HELPERS
# --------------------------------------------------

def _get_db(db=None):
    """Return the supplied database or the default MongoDB database."""
    return db if db is not None else get_database()


def _serialize(document):
    """Convert MongoDB document into a Python dictionary."""
    if document is None:
        return None

    document = dict(document)

    if "_id" in document:
        document["_id"] = str(document["_id"])

    return document


def _serialize_many(documents):
    """Convert multiple MongoDB documents into dictionaries."""
    return [_serialize(document) for document in documents]


def _handle_duplicate(error):
    """Raise a readable error for duplicate records."""
    raise ValueError(
        f"Duplicate record: {error}"
    ) from error


# --------------------------------------------------
# 1. USER OPERATIONS
# --------------------------------------------------

def create_user(data, db=None):
    """Create a new user account."""

    validators.validate_user(data)

    database = _get_db(db)

    document = data.copy()

    document.setdefault("is_active", True)
    document.setdefault("created_at", datetime.now(timezone.utc))

    try:
        result = database.users.insert_one(document)

        return _serialize(
            database.users.find_one({"_id": result.inserted_id})
        )

    except DuplicateKeyError as error:
        _handle_duplicate(error)


def get_user_by_id(user_id, db=None):
    """Retrieve a user using user_id."""

    database = _get_db(db)

    return _serialize(
        database.users.find_one({"user_id": user_id})
    )


def get_user_by_email(email, db=None):
    """Retrieve a user using email."""

    database = _get_db(db)

    return _serialize(
        database.users.find_one({"email": email})
    )


# --------------------------------------------------
# 2. STUDENT OPERATIONS
# --------------------------------------------------

def create_student(data, db=None):
    """Create a new student."""

    validators.validate_student(data)

    database = _get_db(db)

    if data.get("parent_id"):
        validators.validate_parent_reference(
            database,
            data["parent_id"]
        )

    document = data.copy()

    try:
        result = database.students.insert_one(document)

        return _serialize(
            database.students.find_one({"_id": result.inserted_id})
        )

    except DuplicateKeyError as error:
        _handle_duplicate(error)


def get_student(student_id, db=None):
    """Retrieve one student."""

    database = _get_db(db)

    return _serialize(
        database.students.find_one({"student_id": student_id})
    )


def get_all_students(db=None):
    """Retrieve all students."""

    database = _get_db(db)

    students = database.students.find().sort("student_id", 1)

    return _serialize_many(students)


def update_student(student_id, update_data, db=None):
    """Update student information."""

    database = _get_db(db)

    allowed_fields = {
        "name",
        "parent_id",
        "attendance",
        "marks",
        "assignments",
        "backlogs",
        "internship_status",
        "placement_status",
        "risk_label"
    }

    if not isinstance(update_data, dict) or not update_data:
        raise ValueError("Update data cannot be empty.")

    invalid_fields = set(update_data) - allowed_fields

    if invalid_fields:
        raise ValueError(
            f"Fields cannot be updated: {invalid_fields}"
        )

    current = database.students.find_one(
        {"student_id": student_id}
    )

    if current is None:
        return None

    updated_data = dict(current)
    updated_data.update(update_data)

    # Validate the complete updated student record.
    validators.validate_student(updated_data)

    if updated_data.get("parent_id"):
        validators.validate_parent_reference(
            database,
            updated_data["parent_id"]
        )

    database.students.update_one(
        {"student_id": student_id},
        {"$set": update_data}
    )

    return get_student(student_id, database)


# --------------------------------------------------
# 3. PARENT OPERATIONS
# --------------------------------------------------

def create_parent(data, db=None):
    """Create a new parent."""

    validators.validate_parent(data)

    database = _get_db(db)

    document = data.copy()

    document.setdefault("email_opt_in", True)
    document.setdefault("created_at", datetime.now(timezone.utc))

    try:
        result = database.parents.insert_one(document)

        return _serialize(
            database.parents.find_one({"_id": result.inserted_id})
        )

    except DuplicateKeyError as error:
        _handle_duplicate(error)


def get_parent(parent_id, db=None):
    """Retrieve a parent using parent_id."""

    database = _get_db(db)

    return _serialize(
        database.parents.find_one({"parent_id": parent_id})
    )


def get_parent_by_student(student_id, db=None):
    """Find the parent associated with a student."""

    database = _get_db(db)

    student = database.students.find_one(
        {"student_id": student_id}
    )

    if student is None:
        return None

    parent_id = student.get("parent_id")

    if not parent_id:
        return None

    return get_parent(parent_id, database)


def update_parent(parent_id, update_data, db=None):
    """Update parent information."""

    database = _get_db(db)

    allowed_fields = {
        "name",
        "phone",
        "email",
        "email_opt_in"
    }

    if not isinstance(update_data, dict) or not update_data:
        raise ValueError("Update data cannot be empty.")

    invalid_fields = set(update_data) - allowed_fields

    if invalid_fields:
        raise ValueError(
            f"Fields cannot be updated: {invalid_fields}"
        )

    current = database.parents.find_one(
        {"parent_id": parent_id}
    )

    if current is None:
        return None

    updated_data = dict(current)
    updated_data.update(update_data)

    validators.validate_parent(updated_data)

    database.parents.update_one(
        {"parent_id": parent_id},
        {"$set": update_data}
    )

    return get_parent(parent_id, database)


# --------------------------------------------------
# 4. MENTOR OPERATIONS
# --------------------------------------------------

def create_mentor(data, db=None):
    """Create a new mentor profile."""

    validators.validate_mentor(data)

    database = _get_db(db)

    document = data.copy()
    document.setdefault("is_active", True)

    try:
        result = database.mentors.insert_one(document)

        return _serialize(
            database.mentors.find_one({"_id": result.inserted_id})
        )

    except DuplicateKeyError as error:
        _handle_duplicate(error)


def get_mentor(mentor_id, db=None):
    """Retrieve mentor profile."""

    database = _get_db(db)

    return _serialize(
        database.mentors.find_one({"mentor_id": mentor_id})
    )


# --------------------------------------------------
# 5. INTERVENTION OPERATIONS
# --------------------------------------------------

def create_intervention(data, db=None):
    """Create a new intervention with pending status."""

    validators.validate_required_fields(
        data,
        ["intervention_id", "student_id", "description"]
    )

    database = _get_db(db)

    validators.validate_student_reference(
        database,
        data["student_id"]
    )

    document = data.copy()

    # New interventions must always start as pending.
    document["status"] = "pending"

    document.setdefault(
        "created_at",
        datetime.now(timezone.utc)
    )

    document.setdefault("reviewed_by", None)
    document.setdefault("reviewed_at", None)
    document.setdefault("mentor_feedback", "")

    validators.validate_intervention(document)

    try:
        result = database.interventions.insert_one(document)

        return _serialize(
            database.interventions.find_one(
                {"_id": result.inserted_id}
            )
        )

    except DuplicateKeyError as error:
        _handle_duplicate(error)


def get_interventions(student_id, db=None):
    """Retrieve all interventions for a student."""

    database = _get_db(db)

    records = database.interventions.find(
        {"student_id": student_id}
    ).sort("created_at", -1)

    return _serialize_many(records)


def get_pending_interventions(db=None):
    """Retrieve all interventions awaiting mentor review."""

    database = _get_db(db)

    records = database.interventions.find(
        {"status": "pending"}
    ).sort("created_at", -1)

    return _serialize_many(records)


def update_intervention_status(
    intervention_id,
    status,
    reviewed_by=None,
    mentor_feedback="",
    db=None
):
    """Update intervention approval or rejection status."""

    database = _get_db(db)

    if status not in validators.INTERVENTION_STATUSES:
        raise ValueError("Invalid intervention status.")

    update_data = {
        "status": status,
        "reviewed_at": datetime.now(timezone.utc),
        "reviewed_by": reviewed_by,
        "mentor_feedback": mentor_feedback
    }

    result = database.interventions.update_one(
        {
            "intervention_id": intervention_id,
            "status": "pending"
        },
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return None

    return _serialize(
        database.interventions.find_one(
            {"intervention_id": intervention_id}
        )
    )

# --------------------------------------------------
# 6. NOTIFICATION OPERATIONS
# --------------------------------------------------

def create_notification(data, db=None):
    """Create one notification record per intervention."""

    if not isinstance(data, dict):
        raise ValueError("Notification data must be a dictionary.")

    database = _get_db(db)

    # Validate notification fields.
    validators.validate_notification(data)

    intervention_id = data["intervention_id"]
    student_id = data["student_id"]
    parent_id = data["parent_id"]

    # Verify student exists.
    student = database.students.find_one(
        {"student_id": student_id}
    )

    if not student:
        raise ValueError("Student not found.")

    # Verify parent exists and is linked to the student.
    parent = database.parents.find_one(
        {"parent_id": parent_id}
    )

    if not parent:
        raise ValueError("Parent not found.")

    if student.get("parent_id") != parent_id:
        raise ValueError("Parent is not linked to this student.")

    # Check parent email notification preference.
    if parent.get("email_opt_in", True) is not True:
        raise ValueError(
            "Parent has not opted in to email notifications."
        )

    # Verify recipient email.
    if parent.get("email") != data["recipient_email"]:
        raise ValueError(
            "Recipient email does not match parent email."
        )

    # Verify intervention exists and is approved.
    intervention = database.interventions.find_one(
        {
            "intervention_id": intervention_id,
            "student_id": student_id,
        }
    )

    if not intervention:
        raise ValueError("Intervention not found.")

    if intervention.get("status") != "approved":
        raise ValueError(
            "Notifications can only be created for approved interventions."
        )

    # Return an existing notification instead of creating a duplicate.
    existing_notification = database.notifications.find_one(
        {"intervention_id": intervention_id}
    )

    if existing_notification:
        return _serialize(existing_notification)

    # Prepare notification record.
    notification = data.copy()

    notification.setdefault("provider_message_id", None)
    notification.setdefault("sent_at", None)
    notification.setdefault("error", None)
    notification.setdefault("attempt_count", 0)
    notification.setdefault(
        "created_at",
        datetime.now(timezone.utc)
    )

    validators.validate_notification(notification)

    try:
        database.notifications.insert_one(notification)

    except DuplicateKeyError:
        # Another request may have created the notification simultaneously.
        existing_notification = database.notifications.find_one(
            {"intervention_id": intervention_id}
        )

        if existing_notification:
            return _serialize(existing_notification)

        raise

    return _serialize(
        database.notifications.find_one(
            {"notification_id": notification["notification_id"]}
        )
    )


def update_notification_status(
    notification_id,
    status,
    provider_message_id=None,
    error=None,
    db=None
):
    """Update email notification delivery status."""

    database = _get_db(db)

    if status not in validators.NOTIFICATION_STATUSES:
        raise ValueError("Invalid notification status.")

    update_data = {
        "status": status,
        "provider_message_id": provider_message_id,
        "error": error
    }

    if status == "sent":
        update_data["sent_at"] = datetime.now(timezone.utc)
    else:
        update_data["sent_at"] = None

    result = database.notifications.update_one(
        {"notification_id": notification_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return None

    return _serialize(
        database.notifications.find_one(
            {"notification_id": notification_id}
        )
    )
    

def get_notifications(student_id, db=None):
    """Retrieve notification history for a student."""

    database = _get_db(db)

    records = database.notifications.find(
        {"student_id": student_id}
    ).sort("sent_at", -1)

    return _serialize_many(records)

