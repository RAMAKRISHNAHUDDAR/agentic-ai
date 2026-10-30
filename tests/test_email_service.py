
import pytest
from unittest.mock import patch, MagicMock

from app.notifications.email_service import (
    send_email,
    EmailConfigurationError,
    EmailDeliveryError,
)


def test_invalid_recipient():
    with pytest.raises(ValueError):
        send_email(
            "invalid-email",
            "Test subject",
            "Test body",
        )


def test_empty_subject():
    with pytest.raises(ValueError):
        send_email(
            "test@example.com",
            "",
            "Test body",
        )


def test_empty_body():
    with pytest.raises(ValueError):
        send_email(
            "test@example.com",
            "Test subject",
            "",
        )


@patch("app.notifications.email_service.os.getenv")
def test_missing_smtp_configuration(mock_getenv):
    mock_getenv.return_value = ""

    with pytest.raises(EmailConfigurationError):
        send_email(
            "test@example.com",
            "Test subject",
            "Test body",
        )


@patch("app.notifications.email_service.smtplib.SMTP")
@patch("app.notifications.email_service._get_email_config")
def test_successful_email_send(mock_config, mock_smtp):

    mock_config.return_value = {
        "server": "smtp.gmail.com",
        "port": 587,
        "email": "sender@gmail.com",
        "password": "test-password",
        "use_tls": True,
    }

    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server
    mock_server.send_message.return_value = {}

    result = send_email(
        "receiver@example.com",
        "Test subject",
        "Test email body",
    )

    assert result["success"] is True
    assert result["recipient"] == "receiver@example.com"

    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()


@patch("app.notifications.email_service.smtplib.SMTP")
@patch("app.notifications.email_service._get_email_config")
def test_smtp_connection_failure(mock_config, mock_smtp):

    mock_config.return_value = {
        "server": "smtp.gmail.com",
        "port": 587,
        "email": "sender@gmail.com",
        "password": "test-password",
        "use_tls": True,
    }

    mock_smtp.side_effect = OSError("Connection failed")

    with pytest.raises(EmailDeliveryError):
        send_email(
            "receiver@example.com",
            "Test subject",
            "Test body",
        )


def test_invalid_smtp_port(monkeypatch):

    monkeypatch.setenv("SMTP_SERVER", "smtp.gmail.com")
    monkeypatch.setenv("SMTP_EMAIL", "sender@gmail.com")
    monkeypatch.setenv("SMTP_PASSWORD", "test-password")
    monkeypatch.setenv("SMTP_PORT", "invalid")
    
    with pytest.raises(EmailConfigurationError):
        send_email(
            "receiver@example.com",
            "Test subject",
            "Test body",
        )
