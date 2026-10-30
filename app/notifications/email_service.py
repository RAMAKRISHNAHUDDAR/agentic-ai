
import os
import re
import ssl
import smtplib
import logging

from pathlib import Path
from email.message import EmailMessage
from email.utils import parseaddr
from dotenv import load_dotenv


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Custom exceptions
# --------------------------------------------------

class EmailConfigurationError(Exception):
    """Raised when email configuration is invalid."""


class EmailDeliveryError(Exception):
    """Raised when an email cannot be delivered."""


# --------------------------------------------------
# Configuration loader
# --------------------------------------------------

def _get_email_config():
    """Load and validate SMTP configuration."""

    smtp_server = os.getenv("SMTP_SERVER", "").strip()
    smtp_email = os.getenv("SMTP_EMAIL", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip()

    if not smtp_server:
        raise EmailConfigurationError(
            "SMTP_SERVER is missing from .env"
        )

    if not smtp_email:
        raise EmailConfigurationError(
            "SMTP_EMAIL is missing from .env"
        )

    if not smtp_password:
        raise EmailConfigurationError(
            "SMTP_PASSWORD is missing from .env"
        )

    try:
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError as error:
        raise EmailConfigurationError(
            "SMTP_PORT must be a valid integer"
        ) from error

    if not 1 <= smtp_port <= 65535:
        raise EmailConfigurationError(
            "SMTP_PORT must be between 1 and 65535"
        )

    use_tls_value = os.getenv(
        "SMTP_USE_TLS", "true"
    ).strip().lower()

    if use_tls_value not in {"true", "false"}:
        raise EmailConfigurationError(
            "SMTP_USE_TLS must be true or false"
        )

    use_tls = use_tls_value == "true"

    if not _is_valid_email(smtp_email):
        raise EmailConfigurationError(
            "SMTP_EMAIL is not a valid email address"
        )

    return {
        "server": smtp_server,
        "port": smtp_port,
        "email": smtp_email,
        "password": smtp_password.replace(" ", ""),
        "use_tls": use_tls,
    }


# --------------------------------------------------
# Email validation
# --------------------------------------------------

def _is_valid_email(email):
    """Perform basic email address validation."""

    if not isinstance(email, str):
        return False

    email = email.strip()

    if not email or len(email) > 254:
        return False

    if "\r" in email or "\n" in email:
        return False

    parsed_name, parsed_email = parseaddr(email)

    if parsed_name or parsed_email != email:
        return False

    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            email
        )
    )


# --------------------------------------------------
# Email sender
# --------------------------------------------------

def send_email(
    to_email,
    subject,
    body,
    html_body=None,
):
    """
    Send an email using configured SMTP credentials.

    Returns:
        dict: Delivery result containing message_id.

    Raises:
        EmailConfigurationError: Invalid SMTP configuration.
        EmailDeliveryError: SMTP delivery failure.
        ValueError: Invalid email input.
    """

    # Validate recipient
    if not _is_valid_email(to_email):
        raise ValueError("Invalid recipient email address")

    # Validate subject
    if not isinstance(subject, str) or not subject.strip():
        raise ValueError("Email subject cannot be empty")

    if "\r" in subject or "\n" in subject:
        raise ValueError("Email subject contains invalid characters")

    # Validate message body
    if not isinstance(body, str) or not body.strip():
        raise ValueError("Email body cannot be empty")

    if html_body is not None and not isinstance(html_body, str):
        raise ValueError("HTML body must be a string")

    config = _get_email_config()

    # Construct email
    message = EmailMessage()

    message["From"] = config["email"]
    message["To"] = to_email.strip()
    message["Subject"] = subject.strip()

    message.set_content(body)

    if html_body:
        message.add_alternative(
            html_body,
            subtype="html"
        )

    message_id = message["Message-ID"]

    try:
        context = ssl.create_default_context()

        # Connect to SMTP server
        with smtplib.SMTP(
            config["server"],
            config["port"],
            timeout=20
        ) as server:

            server.ehlo()

            # Secure the connection
            if config["use_tls"]:
                server.starttls(context=context)
                server.ehlo()

            # Authenticate
            server.login(
                config["email"],
                config["password"]
            )

            # Send email
            refused_recipients = server.send_message(
                message
            )

            if refused_recipients:
                raise EmailDeliveryError(
                    "SMTP server refused the recipient"
                )

        logger.info(
            "Email accepted by SMTP server. Message ID: %s",
            message_id
        )

        return {
            "success": True,
            "message_id": message_id,
            "recipient": to_email.strip(),
        }

    except EmailDeliveryError:
        raise

    except (
        smtplib.SMTPException,
        OSError,
        ssl.SSLError,
        TimeoutError,
    ) as error:

        logger.exception(
            "Email delivery failed for recipient: %s",
            to_email
        )

        raise EmailDeliveryError(
            "Unable to send email. Check SMTP configuration "
            "and server availability."
        ) from error
