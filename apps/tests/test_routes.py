import unittest
from apps import db, app
from apps.models import Post, User

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        app.testing = True
        self.client = app.test_client()
        self.movie = 1
        db.create_all()

        # Create a test user for authentication
        user = User(username="testuser", email="testuser@example.com")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        self.user = user

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

    def test_user(self):
        response = self.client.get(f"/user/{self.user.id}")
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        post = Post(body="Test post", author=self.user, movie_id=self.movie)
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

