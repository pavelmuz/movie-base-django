import tempfile
import uuid

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from drf_spectacular.utils import extend_schema

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Q

from chats.models import Message
from movies.models import Movie, Like, Comment
from notifications.models import Notification
from users.models import Profile, Follow


from .permissions import (IsAuthenticatedOrPatchDeleteOnly, IsMovieOwnerOrReadOnly,
                          IsNotificationRecipientOrReadOnly, IsProfileOwnerOrReadOnly)
from .utils import get_movie, get_movies
from .serializers import (ProfileSerializer, MovieSerializer,
                          NotificationSerializer, MovieCreateSerializer,
                          MessageSerializer, ProfileShortSerializer,
                          UserSerializer)
from .s3 import upload_to_s3


@permission_classes([AllowAny])
class LoginView(APIView):
    @extend_schema(
        description="Войти по имени пользователя и паролю",
        responses={200: {"description": "Login successful"}},
        request={"username": {"type": "string"},
                 "password": {"type": "string"}}
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            profile = Profile.objects.get(user=user)
            serializer = ProfileShortSerializer(profile, many=False)
            return Response({'profile': serializer.data, 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=200)

        return Response({'error': 'Invalid credentials'}, status=400)


class RegisterView(generics.CreateAPIView):
    """Создать аккаунт"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            profile = Profile.objects.get(user=user)
            profile_serializer = ProfileShortSerializer(profile, many=False)
            return Response(
                {
                    'message': "User created",
                    'profile': profile_serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                status=201
            )
        return Response(serializer.errors, status=400)


@permission_classes([IsAuthenticated])
class LogoutView(APIView):
    @extend_schema(
        description="Выход",
        responses={200: {"description": "Logout successful"}},
        request={"refresh_token": {"type": "string"}},
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=200)
        except KeyError as exc:
            raise ParseError('Refresh token is required') from exc
        except TokenError as exc:
            raise ParseError('Invalid token') from exc


class MovieListView(generics.ListAPIView):
    '''Получить главную ленту фильмов'''
    queryset = Movie.objects.all().order_by('-created')
    serializer_class = MovieSerializer


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrPatchDeleteOnly, IsMovieOwnerOrReadOnly])
def movie_view(request, pk):
    movie = Movie.objects.get(id=pk)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=200)
    if request.method == 'PATCH':
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            user_rating = serializer.validated_data.get('user_rating')
            user_review = serializer.validated_data.get('user_review')
            if user_rating is not None:
                movie.user_rating = user_rating
            if user_review is not None:
                movie.user_review = user_review
            movie.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    if request.method == 'DELETE':
        movie.delete()
        return Response({'message': 'Movie deleted'}, status=204)


class AddMovieView(generics.CreateAPIView):
    '''Добавить фильм'''
    queryset = Movie.objects.all()
    serializer_class = MovieCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)


class ProfileListView(generics.ListAPIView):
    '''Получить список пользователей'''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticatedOrPatchDeleteOnly, IsProfileOwnerOrReadOnly])
def account_view(request):
    profile = request.user.profile
    if request.method == 'GET':
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data, status=200)
    if request.method == 'PATCH':
        image = request.FILES.get('image')
        data_copy = request.data.copy()
        if 'image' in request.data:
            del data_copy['image']
        serializer = ProfileSerializer(
            profile, data=data_copy, partial=True)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            birthday = serializer.validated_data.get('birthday')
            if name is not None:
                profile.name = name
            if username is not None:
                profile.username = username
            if email is not None:
                profile.email = email
            if birthday is not None:
                profile.birthday = birthday
            profile.save()
        if image:
            object_name = f"{uuid.uuid4()}-{image.name}"
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                for chunk in image.chunks():
                    temp_file.write(chunk)
                file_path = temp_file.name
            s3_url = upload_to_s3(file_path=file_path, object_name=object_name)
            if s3_url:
                profile.profile_image = s3_url
                profile.save()
        return Response(serializer.data, status=200)
    if request.method == 'DELETE':
        profile.delete()
        return Response({'message': 'Profile deleted'}, status=204)


class AccountFeedListView(generics.ListAPIView):
    '''Получить ленту фильмов пользователя'''
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsMovieOwnerOrReadOnly]

    def get_queryset(self):
        owner = self.request.user.profile
        movies = Movie.objects.filter(owner=owner).order_by('-created')
        return movies

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileFeedListView(generics.ListAPIView):
    '''Получить ленту фильмов пользователя'''
    serializer_class = MovieSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        owner = Profile.objects.get(id=pk)
        movies = Movie.objects.filter(owner=owner).order_by('-created')
        return movies

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NotificationListView(generics.ListAPIView):
    '''Получить список уведомлений'''
    serializer_class = NotificationSerializer
    permission_classes = [IsNotificationRecipientOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        profile = self.request.user.profile
        notifications = profile.notifications.all().order_by('-created')
        return notifications

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NotificationView(generics.DestroyAPIView):
    '''Удалить уведомление'''
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [
        IsAuthenticatedOrPatchDeleteOnly,
        IsNotificationRecipientOrReadOnly
    ]


class ActiveChatsListView(generics.ListAPIView):
    '''Получить список активных чатов'''
    serializer_class = ProfileShortSerializer
    permission_classes = [IsAuthenticatedOrPatchDeleteOnly]

    def get_queryset(self):
        profile = self.request.user.profile
        active_chats = Profile.objects.filter(
            Q(sent_messages__recipient=profile) |
            Q(recieved_messages__sender=profile)
        ).distinct()
        return active_chats

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChatListView(generics.ListAPIView):
    '''Получить список сообщений в чате'''
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrPatchDeleteOnly]

    def get_queryset(self):
        recipient_id = self.kwargs.get('recipient_id')
        current_user = self.request.user.profile
        recipient = Profile.objects.get(id=recipient_id)
        messages = Message.objects.filter(
            (Q(sender=current_user) & Q(recipient=recipient)) |
            (Q(sender=recipient) & Q(recipient=current_user))
        ).order_by('timestamp')
        return messages

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def like_view(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    owner = request.user.profile
    if request.method == 'POST':
        Like.objects.create(
            owner=owner,
            movie=movie
        )
        return Response({'message': 'Like created'}, status=201)
    if request.method == 'DELETE':
        try:
            like = movie.like_set.get(owner=owner)
            like.delete()
            return Response({'message': 'Like deleted'}, status=204)
        except:
            return Response({'message': 'Like not found'}, status=404)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def follow_view(request, profile_id):
    follower = request.user.profile
    following = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        Follow.objects.create(
            follower=follower,
            following=following
        )
        return Response({'message': 'Follow created'}, status=201)
    if request.method == 'DELETE':
        try:
            follow = follower.follower_set.get(following=following)
            follow.delete()
            return Response({'message': 'Follow deleted'}, status=204)
        except:
            return Response({'message': 'Follow not found'}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def message_view(request, recipient_id):
    sender = request.user.profile
    recipient = Profile.objects.get(id=recipient_id)
    body = request.data.get('message')
    Message.objects.create(
        sender=sender,
        recipient=recipient,
        body=body
    )
    return Response({'mesasge': 'Message sent'}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_view(request, movie_id):
    owner = request.user.profile
    movie = Movie.objects.get(id=movie_id)
    body = request.data.get('comment')
    Comment.objects.create(
        owner=owner,
        movie=movie,
        body=body
    )
    return Response({'message': 'Comment sent'}, status=201)


@extend_schema(
    description='Получить список фильмов по ключевому слову',
    responses={"200": {"description": "List of movies"}},
)
@api_view(['GET'])
def get_kinopoisk_movies(request, title: str):
    cache_key = f'movie_search_{title}'
    cached_movies = cache.get(cache_key)

    if cached_movies is None:
        movies = get_movies(title)
        cache.set(cache_key, movies, 60*15)
    else:
        movies = cached_movies
    return Response(movies)


@extend_schema(
    description='Получить данные о фильме по ID',
    responses={"200": {"description": "Movie details"}},
)
@api_view(['GET'])
def get_kinopoisk_movie(request, kinopoisk_id: int):
    cache_key = f'kinopoisk_{kinopoisk_id}'
    cached_movie = cache.get(cache_key)

    if cached_movie is None:
        movie = get_movie(kinopoisk_id)
        cache.set(cache_key, movie, 60*15)
    else:
        movie = cached_movie
    return Response(movie)
