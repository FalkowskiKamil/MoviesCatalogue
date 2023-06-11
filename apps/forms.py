from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerRangeField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    """
    Form for user registration.
    """
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """
    Form for user login.
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class PostForm(FlaskForm):
    """
    Form for creating a new post.
    """
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Post")


class RateForm(FlaskForm):
    """
    Form for rating a movie.
    """
    rate = IntegerRangeField("Rate", validators=[DataRequired(), NumberRange(min=1, max=10)], default="6")
    submit = SubmitField("Add Rate")


class CommentForm(FlaskForm):
    """
    Form for adding a comment to a post.
    """
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Comment")


class FavoriteForm(FlaskForm):
    """
    Form for marking a movie as favorite.
    """
    favorite = SubmitField("Favorite")