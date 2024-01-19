from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification
from .models import Like, Comment


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.movie.owner,
            sender=instance.owner,
            notification_type='like',
            movie=instance.movie
        )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.movie.owner,
            sender=instance.owner,
            notification_type='comment',
            movie=instance.movie
        )
