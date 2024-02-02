from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import Profile, Follow
from movies.models import Movie
from .serializers import (ProfileSerializer, MovieSerializer,
                          LikeSerializer, CommentSerializer,
                          FollowSerializer, NotificationSerializer)


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
        {'GET': 'notifications/:id'}
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
