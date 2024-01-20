from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from .models import Message


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.recipient,
            sender=instance.sender,
            notification_type='message',
            message=instance
        )
