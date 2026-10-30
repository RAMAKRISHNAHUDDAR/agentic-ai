
import pytest
from unittest.mock import patch

from app.safety import approval


# --------------------------------------------------
# TEST DATA
# --------------------------------------------------

STUDENT_ID = "STU378"
INTERVENTION_ID = "INT001"
PARENT_ID = "PAR378"
PARENT_EMAIL = "parent@example.com"

PENDING_INTERVENTION = {
    "intervention_id": INTERVENTION_ID,
    "student_id": STUDENT_ID,
    "description": "Improve attendance and academic performance",
    "status": "pending",
    "mentor_feedback": "",
}

APPROVED_INTERVENTION = {
    **PENDING_INTERVENTION,
    "status": "approved",
    "mentor_feedback": "Approved by mentor",
}

STUDENT = {
    "student_id": STUDENT_ID,
    "name": "Test Student",
    "parent_id": PARENT_ID,
}

PARENT = {
    "parent_id": PARENT_ID,
    "name": "Test Parent",
    "email": PARENT_EMAIL,
    "email_opt_in": True,
}

NOTIFICATION = {
    "notification_id": "EMAIL_INT001",
    "intervention_id": INTERVENTION_ID,
    "student_id": STUDENT_ID,
    "parent_id": PARENT_ID,
    "recipient_email": PARENT_EMAIL,
    "status": "pending",
}


# --------------------------------------------------
# HELPER
# --------------------------------------------------

def setup_approval_mocks():
    """Prepare common mocks for an intervention approval."""

    patches = [
        patch(
            "app.safety.approval.get_interventions",
            return_value=[PENDING_INTERVENTION.copy()]
        ),
        patch(
            "app.safety.approval.update_intervention_status",
            return_value=APPROVED_INTERVENTION.copy()
        ),
        patch(
            "app.safety.approval.get_student",
            return_value=STUDENT.copy()
        ),
        patch(
            "app.safety.approval.get_parent_by_student",
            return_value=PARENT.copy()
        ),
        patch(
            "app.safety.approval.create_notification",
            return_value=NOTIFICATION.copy()
        ),
        patch(
            "app.safety.approval.send_email",
            return_value={
                "success": True,
                "message_id": "mock-message-001",
                "recipient": PARENT_EMAIL,
            }
        ),
        patch(
            "app.safety.approval.update_notification_status",
            return_value={
                **NOTIFICATION,
                "status": "sent",
            }
        ),
        patch("app.safety.approval.log_action"),
    ]

    mocks = [p.start() for p in patches]

    return patches, mocks


def stop_patches(patches):
    for p in patches:
        p.stop()


# --------------------------------------------------
# TEST 1: APPROVAL SENDS EMAIL
# --------------------------------------------------

def test_approval_sends_parent_email():

    patches, mocks = setup_approval_mocks()

    try:
        send_email_mock = mocks[5]

        result = approval.approve_intervention(
            STUDENT_ID,
            PENDING_INTERVENTION["description"],
            "Approved by mentor"
        )

        send_email_mock.assert_called_once()

        assert result is not None

    finally:
        stop_patches(patches)


# --------------------------------------------------
# TEST 2: REJECTION DOES NOT SEND EMAIL
# --------------------------------------------------

def test_rejection_does_not_send_email():

    with patch(
        "app.safety.approval.get_interventions",
        return_value=[PENDING_INTERVENTION.copy()]
    ), patch(
        "app.safety.approval.update_intervention_status",
        return_value={
            **PENDING_INTERVENTION,
            "status": "rejected",
        }
    ), patch(
        "app.safety.approval.log_action"
    ), patch(
        "app.safety.approval.send_email"
    ) as send_email_mock:

        result = approval.reject_intervention(
            STUDENT_ID,
            PENDING_INTERVENTION["description"],
            "Not suitable"
        )

        send_email_mock.assert_not_called()

        assert result is not None


# --------------------------------------------------
# TEST 3: ALREADY SENT EMAIL IS NOT SENT AGAIN
# --------------------------------------------------

def test_already_sent_notification_is_not_resent():

    patches, mocks = setup_approval_mocks()

    try:
        create_notification_mock = mocks[4]
        send_email_mock = mocks[5]

        create_notification_mock.return_value = {
            **NOTIFICATION,
            "status": "sent",
        }

        approval.approve_intervention(
            STUDENT_ID,
            PENDING_INTERVENTION["description"],
            "Approved by mentor"
        )

        send_email_mock.assert_not_called()

    finally:
        stop_patches(patches)


# --------------------------------------------------
# TEST 4: EMAIL FAILURE DOES NOT UNDO APPROVAL
# --------------------------------------------------

def test_email_failure_does_not_undo_approval():

    patches, mocks = setup_approval_mocks()

    try:
        send_email_mock = mocks[5]
        update_status_mock = mocks[6]

        send_email_mock.side_effect = Exception(
            "Simulated SMTP failure"
        )

        result = approval.approve_intervention(
            STUDENT_ID,
            PENDING_INTERVENTION["description"],
            "Approved by mentor"
        )

        # Approval should still be successful.
        assert result is not None

        # Email delivery should be marked failed.
        update_status_mock.assert_called()

        failed_call = update_status_mock.call_args

        assert failed_call.kwargs["status"] == "failed"

    finally:
        stop_patches(patches)


# --------------------------------------------------
# TEST 5: PARENT OPTED OUT
# --------------------------------------------------

def test_parent_opt_out_prevents_email():

    patches, mocks = setup_approval_mocks()

    try:
        parent_mock = mocks[3]
        send_email_mock = mocks[5]

        parent_mock.return_value = {
            **PARENT,
            "email_opt_in": False,
        }

        approval.approve_intervention(
            STUDENT_ID,
            PENDING_INTERVENTION["description"],
            "Approved by mentor"
        )

        send_email_mock.assert_not_called()

    finally:
        stop_patches(patches)
