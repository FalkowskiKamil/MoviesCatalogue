from datetime import datetime
from flask_login import UserMixin
from apps import db
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """
    User model representing a user in the application.

    Inherits from UserMixin and db.Model.

    Attributes:
        id (int): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        posts (List[Post]): The list of posts created by the user.
        ratings (List[Rating]): The list of ratings given by the user.
        favorites (List[Favorite]): The list of movies marked as favorites by the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    rate = db.relationship("Rating", backref="reviewer", lazy="dynamic")
    comment = db.relationship("PostComment", backref="commentator", lazy="dynamic")
    favorite = db.relationship("Favorite", backref="fan", lazy="dynamic")

    def __str__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        # Set the password for the user
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Check if the provided password matches the user"s password
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    """
    Post model representing a user's post about a movie.

    Inherits from db.Model.

    Attributes:
        id (int): The unique identifier of the post.
        body (str): The content of the post.
        timestamp (datetime): The timestamp of when the post was created.
        user_id (int): The ID of the user who created the post.
        movie_id (int): The ID of the movie associated with the post.
        comments (List[PostComment]): The list of comments on the post.
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    movie_id = db.Column(db.Integer, index=True)
    comment = db.relationship("PostComment", backref="topic", lazy="dynamic")

    def __str__(self):
        return f"<Post {self.id} {self.body[:50]} ...>"

class Rating(db.Model):
    """
    Model representing a rating given by a user to a movie.
    """
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    movie_id = db.Column(db.Integer, index=True)
    # Define a unique constraint on user_id and movie_id to ensure each user can rate a movie only once
    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="unique_user_movie"),
    )

    def __str__(self):
        """
        Returns a string representation of the Rating object.

        Returns:
            str: String representation of the Rating object.
        """
        return f"<Rate {self.rate}, by {self.user_id}>"


class PostComment(db.Model):
    """
    Model representing a comment on a post.
    """
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))

    def __str__(self):
        """
        Returns a string representation of the PostComment object.

        Returns:
            str: String representation of the PostComment object.
        """
        return f"<Comment: '{self.body}' "


class Favorite(db.Model):
    """
    Model representing a favorite movie entry for a user.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    movie_id = db.Column(db.Integer, index=True)
    status = db.Column(db.Boolean)
    # Define a unique constraint on user_id and movie_id to ensure each user can have a favorite entry for a movie only once
    __table_args__ = (
        UniqueConstraint("user_id", "movie_id", name="unique_user_movie_fav"),
    )