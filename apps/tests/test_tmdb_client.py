import unittest
from unittest.mock import patch
from apps import tmdb_client


class TmbdbClientTestCase(unittest.TestCase):
    def setUp(self):
        self.api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMmE2Yjg2OTZhYjgzYTNiZTk0OGJjNmViOWJhNmRhNyIsInN1YiI6IjYzOTFjNmIxMTg4NjRiMDA5NDhhYzViMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.5-Dm2PmFrP7Ufwud07spOpIjphx0gkzyxGc5GOzgDio"

    @patch("requests.get")
    def test_get_movies_list(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"results": ["movie1", "movie2"]}
        result = tmdb_client.get_movies_list("popular")
        mock_get.assert_called_once_with(
            "https://api.themoviedb.org/3/movie/popular",
            headers={"Authorization": f"Bearer {self.api_token}"},
        )
        self.assertEqual(result, {"results": ["movie1", "movie2"]})

    @patch("requests.get")
    def test_get_movies(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"results": ["movie1", "movie2", "movie3"]}
        result = tmdb_client.get_movies(2, "popular")
        mock_get.assert_called_once_with(
            "https://api.themoviedb.org/3/movie/popular",
            headers={"Authorization": f"Bearer {self.api_token}"},
        )
        self.assertEqual(result, ["movie1", "movie2"])

    def test_get_poster_url(self):
        poster_api_path = "/path/to/poster.jpg"
        result = tmdb_client.get_poster_url(poster_api_path)
        expected_url = "https://image.tmdb.org/t/p/w342//path/to/poster.jpg"
        self.assertEqual(result, expected_url)

    @patch("requests.get")
    def test_get_single_movie(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"title": "Movie Title"}
        result = tmdb_client.get_single_movie("12345")
        mock_get.assert_called_once_with(
            "https://api.themoviedb.org/3/movie/12345",
            headers={"Authorization": f"Bearer {self.api_token}"},
        )
        self.assertEqual(result, {"title": "Movie Title"})

    @patch("requests.get")
    def test_get_single_movie_cast(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"cast": ["actor1", "actor2"]}
        result = tmdb_client.get_single_movie_cast("12345")
        mock_get.assert_called_once_with(
            "https://api.themoviedb.org/3/movie/12345/credits",
            headers={"Authorization": f"Bearer {self.api_token}"},
        )
        self.assertEqual(result, ["actor1", "actor2"])

    @patch("requests.get")
    def test_get_movie_images(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"backdrops": ["image1.jpg", "image2.jpg"]}
        result = tmdb_client.get_movie_images("12345")
        mock_get.assert_called_once_with(
            "https://api.themoviedb.org/3/movie/12345/images",
            headers={"Authorization": f"Bearer {self.api_token}"},
        )
        self.assertEqual(result, ["image1.jpg", "image2.jpg"])

    @patch("requests.get")
    def test_search_movie(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"results": ["movie1", "movie2"]}
        result = tmdb_client.search_movie("query")
        mock_get.assert_called_once_with(
            "https://api.themoviedb.org/3/search/movie?&query=query",
            headers={"Authorization": f"Bearer {self.api_token}"},
        )
        self.assertEqual(result, {"results": ["movie1", "movie2"]})

    @patch("requests.get")
    def test_live(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"results": ["show1", "show2"]}
        result = tmdb_client.live()
        mock_get.assert_called_once_with(
            "https://api.themoviedb.org/3/tv/airing_today",
            headers={"Authorization": f"Bearer {self.api_token}"},
        )
        self.assertEqual(result, ["show1", "show2"])
