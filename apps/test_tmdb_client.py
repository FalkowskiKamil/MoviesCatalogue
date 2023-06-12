import unittest
from unittest.mock import patch
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerRangeField,
    TextAreaField,
)
from apps import tmdb_client, db, app
from werkzeug.security import  check_password_hash
from .models import *
from .forms import *
from .routes import *
from .data_manager import *
from .routes import *


class Tmbdb_ClientTestCase(unittest.TestCase):
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

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('testpassword')

    def test_set_password(self):
        # Test the set_password method
        self.user.set_password('newpassword')
        self.assertNotEqual(self.user.password_hash, 'newpassword')
        self.assertTrue(check_password_hash(self.user.password_hash, 'newpassword'))

    def test_check_password(self):
        # Test the check_password method
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertFalse(self.user.check_password('wrongpassword'))

    def test_str_representation(self):
        # Test the __str__ method
        self.assertEqual(str(self.user), "<User testuser>")

    def test_post(self):
        # Test the creation of a Post object
        post = Post(body='Test post', author=self.user)
        self.assertEqual(post.body, 'Test post')
        self.assertEqual(post.author, self.user)

    def test_rating(self):
        # Test the creation of a Rating object
        rating = Rating(rate=5, reviewer=self.user)
        self.assertEqual(rating.rate, 5)
        self.assertEqual(rating.reviewer, self.user)

    def test_comment(self):
        # Test the creation of a PostComment object
        comment = PostComment(body='Test comment', commentator=self.user)
        self.assertEqual(comment.body, 'Test comment')
        self.assertEqual(comment.commentator, self.user)

    def test_favorite(self):
        # Test the creation of a Favorite object
        favorite = Favorite(fan=self.user)
        self.assertEqual(favorite.fan, self.user)

class FormTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test database
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Clean up the test database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_comment_form(self):
        with self.app.test_request_context():
            form = CommentForm()            
            self.assertIsInstance(form.body, TextAreaField)
            self.assertIsInstance(form.submit, SubmitField)

    def test_favorite_form(self):
        with self.app.test_request_context():
            form = FavoriteForm()
            self.assertIsInstance(form.favorite, SubmitField)


    def test_login_form(self):
        with self.app.test_request_context():
            form = LoginForm()
            self.assertIsInstance(form.username, StringField)
            self.assertIsInstance(form.password, PasswordField)
            self.assertIsInstance(form.remember, BooleanField)
            self.assertIsInstance(form.submit, SubmitField)

    def test_post_form(self):
        with self.app.test_request_context():
            form = PostForm()
            self.assertIsInstance(form.body, TextAreaField)
            self.assertIsInstance(form.submit, SubmitField)


    def test_rate_form(self):
        with self.app.test_request_context():
            form = RateForm()
            self.assertIsInstance(form.rate, IntegerRangeField)
            self.assertIsInstance(form.submit, SubmitField)


    def test_registration_form(self):
        with self.app.test_request_context():
            form = RegistrationForm()
            self.assertIsInstance(form.username, StringField)
            self.assertIsInstance(form.email, StringField)
            self.assertIsInstance(form.password, PasswordField)
            self.assertIsInstance(form.password2, PasswordField)
            self.assertIsInstance(form.submit, SubmitField)

class UserManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        app.testing = True
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        response = self.client.post(
            "/register",
            data={
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "password",
                "confirm_password": "password",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        with app.app_context():
            user = User(username="testuser", email="testuser@example.com")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

        response = self.client.post(
            "/login",
            data={"username": "testuser", "password": "password"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        # Create a user for testing
        with app.app_context():
            user = User(username="testuser", email="testuser@example.com")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

            # Log in the user
            self.client.post(
                "/login",
                data={"username": "testuser", "password": "password"},
                follow_redirects=True,
            )

            # Send a GET request to the logout route
            response = self.client.get("/logout", follow_redirects=True)
            self.assertEqual(response.status_code, 401)

class DataManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.movie = 1
        self.app_context.push()
        app.testing = True
        self.client = app.test_client()

        db.create_all()

        # Create a test user for authentication
        user = User(username="testuser", email="testuser@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        self.client.post(
            "/login",
            data={"username": "testuser", "password": "password"},
            follow_redirects=True,
        )

    def test_add_comment(self):
        self.login()
        post = Post(body="Test Post", user_id=1, movie_id=self.movie)
        db.session.add(post)
        db.session.commit()

        # Submit a comment form
        response = self.client.post(
            f"/post/{post.id}/comment",
            data={"body": "Test Comment"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

    def test_add_post(self):
        self.login()
        # Submit a post form
        response = self.client.post(
            f"/movie/{self.movie}/post",
            data={"body": "Test Post"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

    def test_add_rate(self):
        self.login()

        # Submit a rate form
        response = self.client.post(
            f"/movie/{self.movie}/rate",
            data={"rate": 5},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

    def test_add_favorite(self):
        self.login()
        # Submit a favorite form
        response = self.client.post(
            f"/movie/{self.movie}/favorite",
            data={"status": True},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        app.testing = True
        self.client = app.test_client()
        self.movie=1
        db.create_all()

        # Create a test user for authentication
        user = User(username="testuser", email="testuser@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        self.user=user
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_movie_details(self):
        response = self.client.get(f"/movie/{self.movie}")
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.client.get("/search?query=test")
        self.assertEqual(response.status_code, 200)

    def test_live(self):
        response = self.client.get("/live")
        self.assertEqual(response.status_code, 200)

    def test_user(self):
        response = self.client.get(f"/user/{self.user.id}")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        post = Post(body='Test post', author=self.user, movie_id=self.movie)
        db.session.add(post)
        db.session.commit()

        response = self.client.get(f"/post/{post.id}")
        self.assertEqual(response.status_code, 200)

    def test_movie_post(self):
        response = self.client.get(f"/movie_post/{self.movie}/{self.user.id}")
        self.assertEqual(response.status_code, 200)

    def test_favorite(self):
        response = self.client.get(f"/favorite/{self.user.id}")
        self.assertEqual(response.status_code, 200)

    def test_all_rates(self):
        response = self.client.get(f"/rates/{self.user.id}")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
