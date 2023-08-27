import unittest
from apps import db, app
from apps.models import Post, User


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
