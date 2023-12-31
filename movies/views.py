from django.shortcuts import render

# Create your views here.


def movies_view(request):
    return render(request, 'movies/movies.html')
