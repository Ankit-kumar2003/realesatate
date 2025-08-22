from flask import current_app, render_template
from flask_mail import Message
from extensions import mail
import secrets
from datetime import datetime, timedelta


def generate_verification_token():
    """Generate a secure random token for email verification."""
    return secrets.token_urlsafe(32)


def send_verification_email(user):
    """Send verification email to user."""
    token = generate_verification_token()
    user.verification_token = token
    user.verification_token_expires = datetime.utcnow() + timedelta(hours=24)

    msg = Message(
        "Verify Your Email - Real Estate",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[user.email],
    )

    # Create verification URL
    verification_url = f"{current_app.config['BASE_URL']}/verify-email/{token}"

    # Render email template
    msg.html = render_template(
        "email/verify_email.html", user=user, verification_url=verification_url
    )

    try:
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send verification email: {str(e)}")
        return False


def send_welcome_email(user):
    """Send welcome email to user after successful verification."""
    msg = Message(
        "Welcome to Real Estate!",
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        recipients=[user.email],
    )

    msg.html = render_template("email/welcome.html", user=user)

    try:
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to send welcome email: {str(e)}")
        return False
