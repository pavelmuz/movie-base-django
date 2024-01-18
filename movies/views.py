from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie
from .utils import get_movies, get_movie, like_movie, unlike_movie, handle_liking_feed, add_comment
from .forms import MovieForm, CommentForm


def feed(request):
    movies = Movie.objects.all().order_by('-created')
    form = CommentForm()
    handle_liking_feed(request, movies, 'movies')
    add_comment(request, movies, 'movies')
    context = {
        'movies': movies,
        'form': form
    }
    return render(request, 'movies/movies.html', context)


def single_movie(request, pk):
    movie = Movie.objects.get(id=pk)
    movie_comments = movie.comment_set.filter(movie=movie).order_by('created')
    form = CommentForm()

    if request.method == 'POST':
        if movie.title in request.POST:
            if request.user.profile.id in movie.users_liked:
                unlike_movie(request, movie)
                return redirect('movie', movie.id)
            else:
                like_movie(
                    profile=request.user.profile,
                    movie=movie
                )
                return redirect('movie', movie.id)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.owner = request.user.profile
                comment.movie = movie
                comment.save()
                return redirect('movie', movie.id)

    context = {
        'movie': movie,
        'comments': movie_comments,
        'form': form
    }
    return render(request, 'movies/movie.html', context)


@login_required(login_url='login')
def search_movies(request):

    if request.method == 'POST':
        if request.POST['movie-title']:
            query = request.POST['movie-title']
            return redirect('search-results', query=query)
        return redirect('search-movies')

    return render(request, 'movies/search-movies.html')


@login_required(login_url='login')
def search_results(request, query):
    movies = get_movies(query)
    context = {
        'movies': movies
    }
    return render(request, 'movies/search-results.html', context)


@login_required(login_url='login')
def add_movie(request, kinopoisk_id):
    movie_found = get_movie(kinopoisk_id)
    profile = request.user.profile
    form = MovieForm()

    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.owner = profile
            movie.title = movie_found['nameRu']
            movie.description = movie_found['description']
            movie.poster_url = movie_found['posterUrl']
            movie.kinopoisk_url = movie_found['webUrl']
            movie.save()
            return redirect('movies')

    context = {
        'movie': movie_found,
        'form': form
    }
    return render(request, 'movies/add-movie.html', context)


@login_required(login_url='login')
def edit_movie(request, pk):
    profile = request.user.profile
    movie = profile.movie_set.get(id=pk)
    form = MovieForm(instance=movie)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        'movie': movie,
        'form': form
    }
    return render(request, 'movies/edit-movie.html', context)


@login_required(login_url='login')
def delete_movie(request, pk):
    profile = request.user.profile
    movie = profile.movie_set.get(id=pk)

    if request.method == 'POST':
        movie.delete()
        return redirect('account')

    context = {
        'movie': movie,
        'delete': 'movie'
    }
    return render(request, 'delete-template.html', context)
