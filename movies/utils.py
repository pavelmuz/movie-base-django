import os
import requests
from dotenv import load_dotenv
from django.shortcuts import redirect
from .models import Like


load_dotenv()

API_HEADERS = {
    'X-API-KEY': os.getenv('KINOPOISK_API_KEY')
}
SEARCH_URL = os.getenv('API_ENDPOINT')


def get_movies(query):
    search_params = {
        'keyword': query
    }
    timeout = (5, 20)

    try:
        resp = requests.get(url=SEARCH_URL, headers=API_HEADERS,
                            params=search_params, timeout=timeout)
    except requests.exceptions.RequestException as e:
        print(f'An error has occured: {e}')

    movies_found = resp.json()['items']
    return movies_found


def get_movie(kinopoisk_id):
    timeout = (5, 20)

    try:
        resp = requests.get(url=f'{SEARCH_URL}/{kinopoisk_id}',
                            headers=API_HEADERS, timeout=timeout)
    except requests.exceptions.RequestException as e:
        print(f'An error has occured: {e}')

    movie = resp.json()
    return movie


def like_movie(profile, movie):
    Like.objects.create(
        owner=profile,
        movie=movie
    )


def unlike_movie(request, movie):
    like = movie.like_set.filter(owner=request.user.profile.id)
    like.delete()


def handle_liking_feed(request, movies, redirect_page):
    if request.method == 'POST':
        for movie in movies:
            if movie.title in request.POST:
                if request.user.profile.id in movie.users_liked:
                    unlike_movie(request, movie)
                    return redirect(redirect_page)
                else:
                    like_movie(
                        profile=request.user.profile,
                        movie=movie
                    )
                    return redirect(redirect_page)
