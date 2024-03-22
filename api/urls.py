from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from .import views


urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('logout/', views.LogoutView.as_view()),

    path('feed/', views.MovieListView.as_view()),
    path('movie/<str:pk>/', views.movie_view),
    path('add-movie/', views.AddMovieView.as_view()),
    path('profiles/<str:query>/', views.ProfileListView.as_view()),
    path('account/', views.account_view),
    path('account-feed/', views.AccountFeedListView.as_view()),
    path('profile/<str:pk>/', views.ProfileView.as_view()),
    path('profile-feed/<str:pk>/', views.ProfileFeedListView.as_view()),
    path('notifications/', views.NotificationListView.as_view()),
    path('notification/<str:pk>/', views.NotificationView.as_view()),
    path('active-chats/', views.ActiveChatsListView.as_view()),
    path('chat/<str:recipient_id>/', views.ChatListView.as_view()),
    path('like/<str:movie_id>/', views.like_view),
    path('follow/<str:profile_id>/', views.follow_view),
    path('message/<str:recipient_id>/', views.message_view),
    path('comment/<str:movie_id>/', views.comment_view),

    path('kinopoisk-movies/<str:title>/', views.get_kinopoisk_movies),
    path('kinopoisk-movie/<str:kinopoisk_id>/', views.get_kinopoisk_movie),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
