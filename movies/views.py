from django.shortcuts import render
from .models import Movie

# Create your views here.


def movies_view(request):
    movies = Movie.objects.all().order_by('title')
    context = {'movies': movies}
    return render(request, 'movies/movies.html', context)
