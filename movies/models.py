import uuid
from django.db import models
from users.models import Profile

# Create your models here.


class Movie(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
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

    @property
    def get_likes(self):
        likes = self.like_set.all()
        return likes.count()

    @property
    def users_liked(self):
        liked = self.like_set.all().values_list('owner__id', flat=True)
        return liked


class Like(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return f'{self.owner.username} liked movie: {self.movie}'
