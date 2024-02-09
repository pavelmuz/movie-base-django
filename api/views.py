from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from users.models import Profile, Follow
from movies.models import Movie
from chats.models import Message
from .utils import get_movie, get_movies
from .serializers import (ProfileSerializer, MovieSerializer,
                          LikeSerializer, CommentSerializer,
                          FollowSerializer, NotificationSerializer,
                          MessageSerializer)


@api_view(['GET'])
def get_routes(request):
    routes = [
        {'GET': 'api/profiles'},
        {'GET': 'api/feed'},
        {'GET': 'api/profile/:id'},
        {'GET': 'api/profile-feed/:id'},
        {'GET': 'api/likes/:id'},
        {'GET': 'api/comments/:id'},
        {'GET': 'api/card-comments/:id'},
        {'GET': 'followers/:id'},
        {'GET': 'followings/:id'},
        {'GET': 'notifications/:id'},
        {'GET': 'active-chats/:id'},
        {'GET': 'chat/:user_id/:recipient_id'}
    ]
    return Response(routes)


@api_view(['GET'])
def get_profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_main_feed(request):
    feed = Movie.objects.all().order_by('-created')
    serializer = MovieSerializer(feed, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_profile_feed(request, pk):
    owner = Profile.objects.get(id=pk)
    feed = Movie.objects.filter(owner=owner)
    serializer = MovieSerializer(feed, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_movie_likes(request, pk):
    movie = Movie.objects.get(id=pk)
    likes = movie.like_set.all()
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_movie_comments(request, pk):
    movie = Movie.objects.get(id=pk)
    comments = movie.comment_set.all().order_by('created')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_movie_card_comments(request, pk):
    movie = Movie.objects.get(id=pk)
    comments = movie.comment_set.all().order_by('-created')[:2]
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_followers(request, pk):
    followers = Follow.objects.filter(following__id=pk)
    serializer = FollowSerializer(followers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_followings(request, pk):
    followings = Follow.objects.filter(follower__id=pk)
    serializer = FollowSerializer(followings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_notifications(request, pk):
    profile = Profile.objects.get(id=pk)
    notifications = profile.notifications.all().order_by('-created')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_active_chats(request, pk):
    profile = Profile.objects.get(id=pk)
    active_chats = Profile.objects.filter(
        Q(sent_messages__recipient=profile) |
        Q(recieved_messages__sender=profile)
    ).distinct()
    serializer = ProfileSerializer(active_chats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_chat(request, user_id, recipient_id):
    current_user = Profile.objects.get(id=user_id)
    recipient = Profile.objects.get(id=recipient_id)
    messages = Message.objects.filter(
        (Q(sender=current_user) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=current_user))
    ).order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def fetch_movies(request, title):
    movies = get_movies(title)
    return Response(movies)


@api_view(['GET'])
def fetch_movie(request, kinopoisk_id):
    movie = get_movie(kinopoisk_id)
    return Response(movie)
