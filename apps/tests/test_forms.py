import unittest
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerRangeField,
    TextAreaField,
)
from apps import db, app
from apps.forms import CommentForm, FavoriteForm, LoginForm, PostForm, RateForm, RegistrationForm

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

    def test_post_form(self):
        with self.app.test_request_context():
            form = PostForm()
            self.assertIsInstance(form.body, TextAreaField)

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

