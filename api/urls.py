from django.urls import path
from .import views

urlpatterns = [
    path('', views.get_routes, name='api'),
    path('profiles/', views.get_profiles),
    path('feed/', views.get_feed)
]
