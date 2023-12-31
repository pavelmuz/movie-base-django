from django.urls import path
from . import views

urlpatterns = [
    path('', views.movies_view, name='movies')
]
