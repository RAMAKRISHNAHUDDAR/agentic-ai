from html import escape
from app.database.repositories import (
    get_interventions,
    update_intervention_status,
)
from app.runtime.audit_logger import log_action

from app.database.repositories import (
    get_parent_by_student,
    get_student,
    create_notification,
    update_notification_status,
)
from app.notifications.email_service import send_email


def _format_intervention(record):
    """Convert a MongoDB intervention into the existing application format."""

    return {
        "intervention_id": record["intervention_id"],
        "student_id": record["student_id"],
        "intervention": record.get(
            "description",
            record.get("intervention", "")
        ),
        "status": record.get("status", "pending"),
        "mentor_feedback": record.get("mentor_feedback", ""),
        "timestamp": record.get(
            "created_at",
            record.get("timestamp", "")
        ),
    }


def _review_intervention(
    student_id,
    intervention,
    status,
    mentor_feedback=""
):
    """Find and review a pending intervention in MongoDB."""

    records = get_interventions(student_id)

    for record in records:
        description = record.get(
            "description",
            record.get("intervention", "")
        )

        if (
            (
                record.get("intervention_id") == intervention
                or description == intervention
            )
            and record.get("status") == "pending"
        ):

            updated_record = update_intervention_status(
                intervention_id=record["intervention_id"],
                status=status,
                reviewed_by="Mentor",
                mentor_feedback=mentor_feedback,
            )

            if updated_record is None:
                return {
                    "error": "Intervention could not be updated."
                }

            action = (
                "approve_intervention"
                if status == "approved"
                else "reject_intervention"
            )

            result = (
                "Approved"
                if status == "approved"
                else "Rejected"
            )

            log_action(
                student_id,
                "Mentor Approval",
                action,
                result
            )

            response = _format_intervention(updated_record)

            if status == "approved":
                response["notification"] = _send_parent_notification(
                    updated_record
                )

            return response

    return {
        "error": "Pending intervention not found"
    }


def approve_intervention(
    student_id,
    intervention,
    mentor_feedback=""
):
    """Approve a pending intervention for a student."""

    return _review_intervention(
        student_id,
        intervention,
        "approved",
        mentor_feedback,
    )


def reject_intervention(
    student_id,
    intervention,
    mentor_feedback=""
):
    """Reject a pending intervention for a student."""

    return _review_intervention(
        student_id,
        intervention,
        "rejected",
        mentor_feedback,
    )




def _send_parent_notification(intervention_record):
    """Send a professional HTML email to the parent after mentor approval."""

    student_id = intervention_record["student_id"]
    intervention_id = intervention_record["intervention_id"]
    notification_id = f"EMAIL_{intervention_id}"

    try:
        student = get_student(student_id)

        if not student:
            return {"status": "failed", "error": "Student not found"}

        parent = get_parent_by_student(student_id)

        if not parent:
            return {"status": "failed", "error": "Parent not found"}

        if not parent.get("email_opt_in", True):
            return {"status": "skipped", "reason": "Parent opted out"}

        recipient = parent.get("email")

        if not recipient:
            return {"status": "failed", "error": "Parent email missing"}

        notification = create_notification({
            "notification_id": notification_id,
            "intervention_id": intervention_id,
            "student_id": student_id,
            "parent_id": parent["parent_id"],
            "recipient_email": recipient,
            "notification_type": "email",
            "status": "pending",
        })

        if not notification:
            return {
                "status": "failed",
                "error": "Notification record could not be created",
            }

        if notification.get("status") == "sent":
            return {
                "status": "already_sent",
                "message": "Parent notification was already sent.",
            }

        # Prepare email information
        student_name = student.get("name", student_id)
        parent_name = parent.get("name", "Parent/Guardian")
        intervention = (
            intervention_record.get("description")
            or intervention_record.get("intervention")
            or "Not provided"
        )
        feedback = (
            intervention_record.get("mentor_feedback")
            or "No additional feedback provided."
        )

        subject = f"Intervention Approval Update - {student_name}"

        # Plain-text fallback
        body = f"""
Dear {parent_name},

We would like to inform you that a mentor has approved an
intervention to support your child's academic progress.

STUDENT DETAILS
Student Name: {student_name}
Student ID: {student_id}

INTERVENTION DETAILS
Intervention: {intervention}

MENTOR FEEDBACK
{feedback}

Thank you for your continued support.

Regards,
Contineo - Student Success Team
"""

        # Escape dynamic values before inserting them into HTML
        safe_parent = escape(str(parent_name))
        safe_student = escape(str(student_name))
        safe_student_id = escape(str(student_id))
        safe_intervention = escape(str(intervention))
        safe_feedback = escape(str(feedback)).replace("\n", "<br>")

        # Professional HTML email
        html_body = f"""
        <html>
        <body style="margin:0; padding:0; background-color:#f4f6f9;
                     font-family:Arial,Helvetica,sans-serif;">

          <table width="100%" cellpadding="0" cellspacing="0"
                 style="padding:30px 12px;">
            <tr>
              <td align="center">

                <table width="100%" cellpadding="0" cellspacing="0"
                       style="max-width:600px; background:#ffffff;
                              border-radius:10px; overflow:hidden;">

                  <tr>
                    <td style="background:#173b65; padding:25px 30px;
                               color:#ffffff;">
                      <h1 style="margin:0; font-size:25px;">
                        CONTINEO
                      </h1>
                      <p style="margin:7px 0 0; font-size:13px;
                                color:#dbeafe;">
                        Student Success &amp; Early Warning System
                      </p>
                    </td>
                  </tr>

                  <tr>
                    <td style="padding:30px; color:#263445;">

                      <h2 style="margin:0 0 20px; color:#173b65;
                                 font-size:22px;">
                        Intervention Approval Update
                      </h2>

                      <p style="font-size:15px; line-height:1.7;">
                        Dear {safe_parent},
                      </p>

                      <p style="font-size:15px; line-height:1.7;">
                        We would like to inform you that a mentor has
                        approved an intervention to support your
                        child's academic progress.
                      </p>

                      <h3 style="color:#173b65; font-size:16px;
                                 margin-top:28px;">
                        Student Information
                      </h3>

                      <table width="100%" cellpadding="10"
                             cellspacing="0"
                             style="background:#f4f7fb;
                                    border-radius:6px;
                                    font-size:14px;">
                        <tr>
                          <td style="color:#64748b;">Student Name</td>
                          <td><strong>{safe_student}</strong></td>
                        </tr>
                        <tr>
                          <td style="color:#64748b;">Student ID</td>
                          <td><strong>{safe_student_id}</strong></td>
                        </tr>
                      </table>

                      <h3 style="color:#173b65; font-size:16px;
                                 margin-top:28px;">
                        Intervention Details
                      </h3>

                      <div style="background:#eff6ff;
                                  border-left:4px solid #2563eb;
                                  padding:16px;
                                  border-radius:5px;
                                  font-size:14px;
                                  line-height:1.7;">
                        {safe_intervention}
                      </div>

                      <h3 style="color:#173b65; font-size:16px;
                                 margin-top:28px;">
                        Mentor Feedback
                      </h3>

                      <div style="background:#f8fafc;
                                  padding:16px;
                                  border-radius:5px;
                                  font-size:14px;
                                  line-height:1.7;">
                        {safe_feedback}
                      </div>

                      <p style="font-size:14px; line-height:1.7;
                                margin-top:28px;">
                        Thank you for your continued support in your
                        child's educational journey.
                      </p>

                      <p style="font-size:14px; line-height:1.7;">
                        Regards,<br>
                        <strong>Contineo - Student Success Team</strong>
                      </p>

                    </td>
                  </tr>

                  <tr>
                    <td style="background:#f1f5f9; padding:18px;
                               text-align:center; color:#64748b;
                               font-size:12px;">
                      This is an automated notification from
                      Contineo Student Success System.
                      <br>
                      Please do not reply directly to this email.
                    </td>
                  </tr>

                </table>
              </td>
            </tr>
          </table>

        </body>
        </html>
        """

        result = send_email(
            to_email=recipient,
            subject=subject,
            body=body,
            html_body=html_body,
        )

        update_notification_status(
            notification_id=notification_id,
            status="sent",
            provider_message_id=result.get("message_id"),
        )

        return {"status": "sent"}

    except Exception:
        try:
            update_notification_status(
                notification_id=notification_id,
                status="failed",
                error="Email delivery failed",
            )
        except Exception:
            pass

        return {"status": "failed", "error": "Email delivery failed"}