from django.conf import settings
from django.core.mail import send_mail

from user.services import build_frontend_url


def send_subscription_confirmation_email(request, subscriber):
    frontend_url = build_frontend_url("subscriptions/confirm", token=subscriber.confirm_token)
    api_url = request.build_absolute_uri(f"/api/v1/subscribe/confirm/{subscriber.confirm_token}/")
    subject = "Confirm your subscription"
    message = (
        "You asked to subscribe to ESG KBTU news.\n\n"
        f"Confirm in the frontend: {frontend_url}\n"
        f"Or use the API confirmation link: {api_url}\n\n"
        "If this was not you, ignore this email."
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscriber.email],
        fail_silently=False,
    )


def send_news_notification_email(news, recipients):
    if not recipients:
        return

    subject = f"News update: {news.title}"
    message = (
        f"{news.digest or ''}\n\n"
        f"Source: {news.site_url}\n"
        f"Read more: {news.ar_site_url or news.site_url}\n\n"
        "You are receiving this email because you confirmed a news subscription."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=False)
