
from app.database.mongodb import get_database


def create_indexes(db=None):
    """
    Create indexes for all six MongoDB collections.

    Unique indexes prevent duplicate records.
    Compound indexes improve frequently used queries.
    """

    if db is None:
        db = get_database()

    # 1. Users collection
    db.users.create_index(
        [("user_id", 1)],
        unique=True,
        name="unique_user_id"
    )

    db.users.create_index(
        [("email", 1)],
        unique=True,
        name="unique_user_email"
    )

    # 2. Students collection
    db.students.create_index(
        [("student_id", 1)],
        unique=True,
        name="unique_student_id"
    )

    # 3. Parents collection
    db.parents.create_index(
        [("parent_id", 1)],
        unique=True,
        name="unique_parent_id"
    )

    # 4. Mentors collection
    db.mentors.create_index(
        [("mentor_id", 1)],
        unique=True,
        name="unique_mentor_id"
    )

    # 5. Interventions collection
    db.interventions.create_index(
        [("intervention_id", 1)],
        unique=True,
        name="unique_intervention_id"
    )

    db.interventions.create_index(
        [("student_id", 1), ("status", 1)],
        name="student_intervention_status"
    )

    # 6. Notifications collection
    db.notifications.create_index(
        [("notification_id", 1)],
        unique=True,
        name="unique_notification_id"
    )

    db.notifications.create_index(
        [("intervention_id", 1), ("status", 1)],
        name="intervention_notification_status"
    )

    db.notifications.create_index(
        [("student_id", 1)],
        name="notification_student_id"
    )

    print("MongoDB indexes created successfully!")


def get_all_indexes(db=None):
    """
    Display all indexes from the six collections.
    """

    if db is None:
        db = get_database()

    collections = [
        "users",
        "students",
        "parents",
        "mentors",
        "interventions",
        "notifications"
    ]

    for collection_name in collections:

        print(f"\nCollection: {collection_name}")

        indexes = db[collection_name].list_indexes()

        for index in indexes:
            print(index["name"], index["key"])
