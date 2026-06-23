from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


def build_frontend_url(path, **params):
    url = f"{settings.FRONTEND_URL.rstrip('/')}/{path.lstrip('/')}"
    if not params:
        return url

    query_string = urlencode(params)
    return f"{url}?{query_string}"


def send_verification_email(request, user):
    token = user.issue_email_verification_token()
    user.email_verification_sent_at = timezone.now()
    user.save(update_fields=["email_verification_token", "email_verification_sent_at"])

    frontend_url = build_frontend_url("verify-email", token=token)
    api_url = request.build_absolute_uri(f"/api/v1/auth/activate/{token}/")
    subject = "Confirm your email"
    message = (
        "Welcome to ESG KBTU.\n\n"
        f"Confirm your email in the frontend: {frontend_url}\n"
        f"Or use the API confirmation link: {api_url}\n\n"
        "If you did not create this account, you can ignore this email."
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_password_reset_email(request, user):
    token = user.issue_password_reset_token()
    user.password_reset_sent_at = timezone.now()
    user.save(update_fields=["password_reset_token", "password_reset_sent_at"])

    frontend_url = build_frontend_url("reset-password", token=token)
    api_url = request.build_absolute_uri(f"/api/v1/auth/password-reset/confirm/{token}/")
    subject = "Reset your password"
    message = (
        "We received a password reset request for your ESG KBTU account.\n\n"
        f"Reset in the frontend: {frontend_url}\n"
        f"Or use the API reset link: {api_url}\n\n"
        "If you did not request a password reset, you can ignore this email."
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
