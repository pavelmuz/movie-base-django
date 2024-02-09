import os
import requests
from dotenv import load_dotenv


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
