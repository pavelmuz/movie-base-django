import uuid
from django.db import models
from users.models import Profile


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='recieved_messages')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)

    def __str__(self):
        return f'{self.sender.username} sent to {self.recipient.username}: {self.body}'
