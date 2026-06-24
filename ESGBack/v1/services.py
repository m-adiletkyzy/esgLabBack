from django.conf import settings
from django.core.mail import send_mail

from user.services import build_frontend_url

from v1.models import Subscriber
from v1.parsers.ESGfilters import is_esg_content
from v1.parsers.NlpMethods import (
    ESG_SUBGENRES,
    classify_news,
    default_genre_preferences,
    should_notify_user,
)


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


def normalize_genre_preferences(preferences):
    if preferences is None:
        return default_genre_preferences()
    if not isinstance(preferences, list):
        raise ValueError("Genre preferences must be a list.")
    invalid = [genre for genre in preferences if genre not in ESG_SUBGENRES]
    if invalid:
        raise ValueError(f"Unsupported sub-genres: {', '.join(invalid)}")
    return list(dict.fromkeys(preferences))


def get_subscriber_genre_preferences(subscriber):
    if subscriber.genre_preferences is None:
        return default_genre_preferences()
    return subscriber.genre_preferences


def get_news_matched_genres(news):
    text = f"{news.title} {news.digest or ''}"
    if news.lang in ('ru', 'kk'):
        return classify_news(text, news.lang)
    return []


def subscriber_should_receive_news(subscriber, news) -> bool:
    preferences = get_subscriber_genre_preferences(subscriber)
    if not preferences:
        return False

    if news.lang in ('ru', 'kk'):
        matched_genres = get_news_matched_genres(news)
        return should_notify_user(preferences, matched_genres)

    return is_esg_content(f"{news.title} {news.digest or ''}", news.lang)


def get_news_notification_recipients(news):
    return [
        subscriber.email
        for subscriber in Subscriber.objects.filter(is_active=True)
        if subscriber_should_receive_news(subscriber, news)
    ]


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
