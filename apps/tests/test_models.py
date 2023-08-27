import unittest
from werkzeug.security import check_password_hash
from apps.models import User, Post, Rating, PostComment, Favorite

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data
        self.user = User(username="testuser", email="test@example.com")
        self.user.set_password("testpassword")

    def test_set_password(self):
        # Test the set_password method
        self.user.set_password("newpassword")
        self.assertNotEqual(self.user.password_hash, "newpassword")
        self.assertTrue(check_password_hash(self.user.password_hash, "newpassword"))

    def test_check_password(self):
        # Test the check_password method
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertFalse(self.user.check_password("wrongpassword"))

    def test_str_representation(self):
        # Test the __str__ method
        self.assertEqual(str(self.user), "<User testuser>")

    def test_post(self):
        # Test the creation of a Post object
        post = Post(body="Test post", author=self.user)
        self.assertEqual(post.body, "Test post")
        self.assertEqual(post.author, self.user)

    def test_rating(self):
        # Test the creation of a Rating object
        rating = Rating(rate=5, reviewer=self.user)
        self.assertEqual(rating.rate, 5)
        self.assertEqual(rating.reviewer, self.user)

    def test_comment(self):
        # Test the creation of a PostComment object
        comment = PostComment(body="Test comment", commentator=self.user)
        self.assertEqual(comment.body, "Test comment")
        self.assertEqual(comment.commentator, self.user)

    def test_favorite(self):
        # Test the creation of a Favorite object
        favorite = Favorite(fan=self.user)
        self.assertEqual(favorite.fan, self.user)
