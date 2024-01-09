from django.shortcuts import render
from .models import Movie

# Create your views here.


def feed(request):
    movies = Movie.objects.all().order_by('-user_rating')
    context = {'movies': movies, 'test': movies[0]}
    return render(request, 'movies/movies.html', context)


def single_movie(request, pk):
    movie = Movie.objects.get(id=pk)
    context = {'movie': movie}
    return render(request, 'movies/movie.html', context)
