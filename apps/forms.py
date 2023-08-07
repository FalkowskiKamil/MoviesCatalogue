from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerRangeField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Enter your username", "class":"form-control form-control-lg"} )
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email", "class":"form-control form-control-lg"} )
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Enter your password", "class":"form-control form-control-lg"} )
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")], render_kw={"placeholder": "Confirm your password", "class":"form-control form-control-lg"} )

    class Meta:
        csrf = False

class LoginForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Enter your username", "class":"form-control form-control-lg"} )
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Enter your password", "class":"form-control form-control-lg"})


class PostForm(FlaskForm):
    
    class Meta:
        csrf = False
    body = TextAreaField("Body", validators=[DataRequired()], render_kw={"placeholder": "Content", "class":"form-control form-control-lg"} )


class RateForm(FlaskForm):
    rate = IntegerRangeField(
        "Rate", validators=[DataRequired(), NumberRange(min=1, max=10)], default="6"
        
    )
    submit = SubmitField("Add Rate", render_kw={"class":"px-auto btn btn-dark mt-2"})
    
    class Meta:
        csrf = False


class CommentForm(FlaskForm):
    body = TextAreaField("Body", validators=[DataRequired()], render_kw={"placeholder": "Content", "class":"form-control"} )
    submit = SubmitField("Comment")
    
    class Meta:
        csrf = False


class FavoriteForm(FlaskForm):
    favorite = SubmitField("Favorite", render_kw={"class":"px-auto btn btn-dark mt-2"})
    
    class Meta:
        csrf = False
