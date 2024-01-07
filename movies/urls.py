from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='movies'),
    path('movie/<str:pk>/', views.single_movie, name='movie')
]
