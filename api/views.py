from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q

from chats.models import Message
from movies.models import Movie
from users.models import Profile


from .utils import get_movie, get_movies
from .serializers import (ProfileSerializer, MovieSerializer, NotificationSerializer,
                          MessageSerializer, ProfileShortSerializer)


@extend_schema(
    description='Получить список фильмов по ключевому слову',
    responses={"200": {"description": "List of movies"}},
)
@api_view(['GET'])
def get_kinopoisk_movies(request, title: str):
    movies = get_movies(title)
    return Response(movies)


@extend_schema(
    description='Получить данные о фильме по ID',
    responses={"200": {"description": "Movie details"}},
)
@api_view(['GET'])
def get_kinopoisk_movie(request, kinopoisk_id: int):
    movie = get_movie(kinopoisk_id)
    return Response(movie)


class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieListView(generics.ListAPIView):
    '''
    Получить главную ленту фильмов
    '''
    queryset = Movie.objects.all().order_by('-created')
    serializer_class = MovieSerializer


class ProfileDetailView(generics.RetrieveAPIView):
    '''
    Получить данные пользователя
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileListView(generics.ListAPIView):
    '''
    Получить список пользователей
    '''
    queryset = Profile.objects.all()
    serializer_class = ProfileShortSerializer


class ProfileFeedListView(generics.ListAPIView):
    '''
    Получить ленту фильмов пользователя
    '''
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
    '''
    Получить список уведомлений
    '''
    serializer_class = NotificationSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        profile = Profile.objects.get(id=pk)
        notifications = profile.notifications.all().order_by('-created')
        return notifications

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ActiveChatsListView(generics.ListAPIView):
    '''
    Получить список активных чатов
    '''
    serializer_class = ProfileShortSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        profile = Profile.objects.get(id=pk)
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
    '''
    Получить список сообщений в чате
    '''
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        recipient_id = self.kwargs.get('recipient_id')
        current_user = Profile.objects.get(id=user_id)
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
            serializer = ProfileSerializer(profile, many=False)
            return Response({'profile': serializer.data, 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=200)

        return Response({'error': 'Invalid credentials'}, status=400)

    @extend_schema(description="Метод запрещен")
    def get(self, request):
        return Response({'error': 'Method not allowed'}, status=405)


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
        except Exception as e:
            return Response({"error": str(e)}, status=400)
