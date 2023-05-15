import requests

# API token for authentication
api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMmE2Yjg2OTZhYjgzYTNiZTk0OGJjNmViOWJhNmRhNyIsInN1YiI6IjYzOTFjNmIxMTg4NjRiMDA5NDhhYzViMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.5-Dm2PmFrP7Ufwud07spOpIjphx0gkzyxGc5GOzgDio"

# Get a list of popular movies
def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

# Get a list of movies based on the specified list type (e.g., popular, top_rated, upcoming)
def get_movies_list(list_type="popular"):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_type}"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

# Get the URL of the movie poster image
def get_poster_url(poster_api_path, size="w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

# Get a specified number of movies based on the list type
def get_movies(how_many, list_type="popular"):
    data = get_movies_list(list_type)
    return data["results"][:how_many]

# Get information about a single movie based on the movie ID
def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

# Get the cast of a single movie based on the movie ID
def get_single_movie_cast(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    if 'cast' in response.json():
        return response.json()["cast"]
    else:
        return None

# Get images associated with a movie based on the movie ID
def get_movie_images(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    if 'backdrops' in response.json():
        return response.json()['backdrops']
    else:
        return []

# Search for movies based on a search query
def search_movie(search_query):
    endpoint = f"https://api.themoviedb.org/3/search/movie?&query={search_query}"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    response = response.json()
    return response

#Get list of TV shows airing today
def live():
    endpoint = f"https://api.themoviedb.org/3/tv/airing_today"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    response=response.json()
    return response['results']

