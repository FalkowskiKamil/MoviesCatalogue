import unittest
from apps import db, app
from apps.models import User


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
            self.assertEqual(response.status_code, 200)
