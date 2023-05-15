from unittest.mock import Mock
import requests
from apps import tmdb_client

def test_get_poster_url_uses_default_size():
   # Przygotowanie danych
   poster_api_path = "some-poster-path"
   expected_default_size = 'w342'
   # Wywołanie kodu, który testujemy
   poster_url = tmdb_client.get_poster_url(poster_api_path=poster_api_path)
   # Porównanie wyników
   assert expected_default_size in poster_url

def test_get_movies_list_type_popular():
   movies_list = tmdb_client.get_movies_list(list_type="popular")
   assert movies_list is not None

def call_tmdb_api(endpoint):
   full_url = f"https://api.themoviedb.org/3/{endpoint}"
   headers = {
       "Authorization": f"Bearer {api_token}"
   }
   response = requests.get(full_url, headers=headers)
   response.raise_for_status()
   return response.json()

def get_movies_list(list_type):
   return call_tmdb_api(f"movie/{list_type}")

def test_get_movies_list_type_popular():
   movies_list = tmdb_client.get_movies_list(list_type="popular")
   assert movies_list is not None

def get_single_movie(movie_id):
   return call_tmdb_api(f'movie/{movie_id}')

def test_get_single_movie_id():
   movie_id=tmdb_client.get_single_movie(movie_id=436270)
   assert movie_id is not None

def get_movie_images(movie_id):
   return call_tmdb_api(f'movie/{movie_id}/images')

def test_get_movie_images():
   movie_id=tmdb_client.get_movie_images(movie_id=436270)
   assert movie_id is not None

def get_single_movie_cast(movie_id):
   return call_tmdb_api(f'movie/{movie_id}/credits')

def test_get_single_movie_cast():
   movie_id=tmdb_client.get_single_movie_cast(movie_id=436270)
   assert movie_id is not None

def test_live():
   movie_list=tmdb_client.live()
   assert movie_list is not None

def test_get_movies_list(monkeypatch):
   # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
   mock_movies_list = ['Movie 1', 'Movie 2']

   requests_mock = Mock()
   # Wynik wywołania zapytania do API
   response = requests_mock.return_value
   # Przysłaniamy wynik wywołania metody .json()
   response.json.return_value = mock_movies_list
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)


   movies_list = tmdb_client.get_movies_list(list_type="popular")
   assert movies_list == mock_movies_list

def test_get_popular_movies(monkeypatch):
   mock_movies_list = ['Movie 1', 'Movie 2']
   requests_mock = Mock()
   response = requests_mock.return_value
   response.json.return_value = mock_movies_list
   monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

   movies_list=tmdb_client.get_movies_list(list_type="popular")
   assert movies_list == mock_movies_list