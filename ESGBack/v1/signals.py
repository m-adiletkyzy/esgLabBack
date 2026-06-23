from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import News, Subscriber
from .services import send_news_notification_email


@receiver(post_save, sender=News)
def send_news_to_subscribers(sender, instance, created, **kwargs):
    if not created:
        return

    recipient_list = list(Subscriber.objects.filter(is_active=True).values_list("email", flat=True))
    send_news_notification_email(instance, recipient_list)
