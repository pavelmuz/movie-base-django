import uuid
from django.db import models

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.IntegerField()
    user_rating = models.FloatField()
    user_review = models.TextField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    poster_url = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    kinopoisk_url = models.CharField(max_length=300)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title
