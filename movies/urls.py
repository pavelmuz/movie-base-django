from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='movies'),
    path('movie/<str:pk>/', views.single_movie, name='movie'),
    path('search-movies/', views.search_movies, name='search-movies'),
    path('select-movie/<str:query>/', views.search_results, name='search-results'),
    path('add-movie/<int:kinopoisk_id>', views.add_movie, name='add-movie')
]
