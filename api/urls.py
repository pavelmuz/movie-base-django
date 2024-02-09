from django.urls import path
from .import views

urlpatterns = [
    path('', views.get_routes, name='api'),
    path('profiles/', views.get_profiles),
    path('feed/', views.get_main_feed),
    path('profile/<str:pk>/', views.get_profile),
    path('profile-feed/<str:pk>/', views.get_profile_feed),
    path('likes/<str:pk>/', views.get_movie_likes),
    path('comments/<str:pk>/', views.get_movie_comments),
    path('card-comments/<str:pk>/', views.get_movie_card_comments),
    path('followers/<str:pk>/', views.get_followers),
    path('followings/<str:pk>/', views.get_followings),
    path('notifications/<str:pk>/', views.get_notifications),
    path('active-chats/<str:pk>/', views.get_active_chats),
    path('chat/<str:user_id>/<str:recipient_id>/', views.get_chat),
    path('movies/<str:title>/', views.fetch_movies),
    path('movie/<str:kinopoisk_id>/', views.fetch_movie)
]
