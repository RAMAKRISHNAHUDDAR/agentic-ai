
from pymongo import MongoClient
#from pymongo.errors import DuplicateKeyError

from app.database.mongodb import MONGODB_URI
from app.database.indexes import create_indexes

from app.database.repositories import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    create_student,
    get_student,
    get_all_students,
    update_student,
    create_parent,
    get_parent,
    get_parent_by_student,
    update_parent,
    create_mentor,
    get_mentor,
    create_intervention,
    get_interventions,
    get_pending_interventions,
    update_intervention_status,
    create_notification,
    update_notification_status,
    get_notifications
)


# Connect to separate test database.
client = MongoClient(MONGODB_URI)

db = client["student_success_test_db"]


def reset_test_database():
    """Clear test collections before running tests."""

    collections = [
        "users",
        "students",
        "parents",
        "mentors",
        "interventions",
        "notifications"
    ]

    for collection_name in collections:
        db[collection_name].delete_many({})

    print("Test database reset successfully!")


# Reset test data and recreate indexes.
reset_test_database()
create_indexes(db)

def run_tests():

    print("\n--- USER TESTS ---")

    user = create_user({
        "user_id": "TEST_USER_001",
        "email": "testuser@example.com",
        "password_hash": "test_hash",
        "role": "student"
    }, db)

    assert user["user_id"] == "TEST_USER_001"
    assert get_user_by_id("TEST_USER_001", db) is not None
    assert get_user_by_email("testuser@example.com", db) is not None

    print("User tests passed!")

    print("\n--- STUDENT TESTS ---")

    student = create_student({
        "student_id": "TEST_STU_001",
        "name": "Test Student",
        "attendance": 85.0,
        "marks": 78.0,
        "assignments": 90.0,
        "backlogs": 0,
        "internship_status": "In Progress",
        "placement_status": "Not Ready",
        "risk_label": 0
    }, db)

    assert student["student_id"] == "TEST_STU_001"
    assert get_student("TEST_STU_001", db) is not None
    assert len(get_all_students(db)) == 1

    updated_student = update_student(
        "TEST_STU_001",
        {"attendance": 90.0},
        db
    )

    assert updated_student["attendance"] == 90.0

    print("Student tests passed!")

    print("\n--- PARENT TESTS ---")

    parent = create_parent({
        "parent_id": "TEST_PAR_001",
        "name": "Test Parent",
        "phone": "+919876543210",
        "email": "testparent@example.com",
        "email_opt_in": True
    }, db)

    assert parent["parent_id"] == "TEST_PAR_001"

    # Link the student to the parent.
    update_student(
        "TEST_STU_001",
        {"parent_id": "TEST_PAR_001"},
        db
    )

    assert get_parent("TEST_PAR_001", db) is not None

    assert get_parent_by_student(
        "TEST_STU_001", db
    )["parent_id"] == "TEST_PAR_001"

    update_parent(
        "TEST_PAR_001",
        {"email_opt_in": False},
        db
    )

    assert get_parent(
        "TEST_PAR_001", db
    )["email_opt_in"] is False

    update_parent(
        "TEST_PAR_001",
        {"email_opt_in": True},
        db
    )

    print("Parent tests passed!")

    print("\n--- MENTOR TESTS ---")

    mentor = create_mentor({
        "mentor_id": "TEST_MENTOR_001",
        "name": "Test Mentor",
        "email": "mentor@example.com",
        "department": "Computer Science"
    }, db)

    assert mentor["mentor_id"] == "TEST_MENTOR_001"
    assert get_mentor("TEST_MENTOR_001", db) is not None

    print("Mentor tests passed!")

    print("\n--- INTERVENTION TESTS ---")

    intervention = create_intervention({
        "intervention_id": "TEST_INT_001",
        "student_id": "TEST_STU_001",
        "description": "Attend additional academic support sessions."
    }, db)

    assert intervention["status"] == "pending"

    assert len(
        get_interventions("TEST_STU_001", db)
    ) == 1

    assert len(get_pending_interventions(db)) == 1

    approved = update_intervention_status(
        "TEST_INT_001",
        "approved",
        reviewed_by="TEST_MENTOR_001",
        mentor_feedback="Approved",
        db=db
    )

    assert approved["status"] == "approved"

    print("Intervention tests passed!")

    print("\n--- NOTIFICATION TESTS ---")

    notification = create_notification({
        "notification_id": "TEST_NOT_001",
        "intervention_id": "TEST_INT_001",
        "student_id": "TEST_STU_001",
        "parent_id": "TEST_PAR_001",
        "recipient_email": "testparent@example.com",
        "notification_type": "email",
        "status": "pending"
    }, db)

    assert notification["status"] == "pending"

    sent = update_notification_status(
        "TEST_NOT_001",
        "sent",
        provider_message_id="TEST_PROVIDER_001",
        db=db
    )

    assert sent["status"] == "sent"
    assert sent["sent_at"] is not None

    assert len(
        get_notifications("TEST_STU_001", db)
    ) == 1

    print("Notification tests passed!")


def run_additional_tests():

    print("\n--- ADDITIONAL VALIDATION TESTS ---")

    # 1. Duplicate student ID must be rejected.
    try:
        create_student({
            "student_id": "TEST_STU_001",
            "name": "Duplicate Student",
            "attendance": 80.0,
            "marks": 80.0,
            "assignments": 80.0,
            "backlogs": 0,
            "internship_status": "In Progress",
            "placement_status": "Not Ready",
            "risk_label": 0
        }, db)

        assert False, "Duplicate student was accepted!"

    except ValueError:
        print("Duplicate student test passed!")

    # 2. Invalid student data must be rejected.
    try:
        create_student({
            "student_id": "TEST_STU_INVALID",
            "name": "Invalid Student",
            "attendance": 150.0,
            "marks": 80.0,
            "assignments": 80.0,
            "backlogs": 0,
            "internship_status": "In Progress",
            "placement_status": "Not Ready",
            "risk_label": 0
        }, db)

        assert False, "Invalid student data was accepted!"

    except ValueError:
        print("Invalid student validation test passed!")

    # 3. Create another pending intervention and reject it.
    rejected_intervention = create_intervention({
        "intervention_id": "TEST_INT_002",
        "student_id": "TEST_STU_001",
        "description": "Create a placement preparation plan."
    }, db)

    assert rejected_intervention["status"] == "pending"

    rejected = update_intervention_status(
        "TEST_INT_002",
        "rejected",
        reviewed_by="TEST_MENTOR_001",
        mentor_feedback="Not required at this time.",
        db=db
    )

    assert rejected["status"] == "rejected"

    print("Intervention rejection test passed!")

    # 4. An already reviewed intervention cannot be updated again.
    second_update = update_intervention_status(
        "TEST_INT_002",
        "approved",
        reviewed_by="TEST_MENTOR_001",
        db=db
    )

    assert second_update is None

    print("Reviewed intervention protection test passed!")

    # 5. Create a pending intervention.
    create_intervention({
        "intervention_id": "TEST_INT_003",
        "student_id": "TEST_STU_001",
        "description": "Improve academic performance."
    }, db)

    # Notification must not be created for pending intervention.
    try:
        create_notification({
            "notification_id": "TEST_NOT_002",
            "intervention_id": "TEST_INT_003",
            "student_id": "TEST_STU_001",
            "parent_id": "TEST_PAR_001",
            "recipient_email": "testparent@example.com",
            "notification_type": "email",
            "status": "pending"
        }, db)

        assert False, "Notification for pending intervention was accepted!"

    except ValueError:
        print("Pending intervention notification protection passed!")

    # 6. Parent email opt-out must block notifications.
    update_parent(
        "TEST_PAR_001",
        {"email_opt_in": False},
        db
    )

    try:
        create_notification({
            "notification_id": "TEST_NOT_003",
            "intervention_id": "TEST_INT_001",
            "student_id": "TEST_STU_001",
            "parent_id": "TEST_PAR_001",
            "recipient_email": "testparent@example.com",
            "notification_type": "email",
            "status": "pending"
        }, db)

        assert False, "Notification was created for opted-out parent!"

    except ValueError:
        print("Parent email opt-out protection passed!")

    print("\nALL ADDITIONAL TESTS PASSED!")


if __name__ == "__main__":
    try:
        run_tests()
        run_additional_tests()

        print("\n================================")
        print("ALL REPOSITORY TESTS PASSED!")
        print("================================")

    finally:
        client.close()
