from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from .import views


urlpatterns = [
    path('kinopoisk-movies/<str:title>/', views.get_kinopoisk_movies),
    path('kinopoisk-movie/<str:kinopoisk_id>/', views.get_kinopoisk_movie),

    path('feed/', views.MovieListView.as_view()),
    path('movie/<str:pk>/', views.MovieDetailView.as_view()),
    path('profiles/', views.ProfileListView.as_view()),
    path('profile/<str:pk>/', views.ProfileDetailView.as_view()),
    path('profile-feed/<str:pk>/', views.ProfileFeedListView.as_view()),
    path('notifications/<str:pk>/', views.NotificationListView.as_view()),
    path('active-chats/<str:pk>/', views.ActiveChatsListView.as_view()),
    path('chat/<str:user_id>/<str:recipient_id>/', views.ChatListView.as_view()),

    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
