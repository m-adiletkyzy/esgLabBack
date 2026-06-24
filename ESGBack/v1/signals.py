from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import News
from .services import get_news_notification_recipients, send_news_notification_email


@receiver(post_save, sender=News)
def send_news_to_subscribers(sender, instance, created, **kwargs):
    if not created:
        return

    recipient_list = get_news_notification_recipients(instance)
    send_news_notification_email(instance, recipient_list)
