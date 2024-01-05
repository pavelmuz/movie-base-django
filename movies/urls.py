from django.urls import path
from . import views

urlpatterns = [
    path('', views.movies_view, name='movies'),
    path('movie/<str:pk>/', views.movie_view, name='movie')
]
