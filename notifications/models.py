import uuid
from django.db import models
from movies.models import Movie
from users.models import Profile


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment')
    )

    recipient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPES)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return f'{self.sender.username} {self.get_notification_type_display()} {self.recipient.username}'
