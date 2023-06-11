from flask import redirect, url_for, render_template, flash
from apps import login_manager, app, db
from flask_login import login_required, login_user, logout_user
from apps.forms import RegistrationForm, LoginForm
from apps.models import User


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user.

    Retrieves the registration data from the submitted form, creates a new `User` object,
    sets the user's password, adds the user to the database, and logs in the newly registered user.

    Redirects to the homepage after successful registration.

    If the form validation fails, the registration form is rendered.

    Returns:
        Response: A redirect response to the homepage or the registration form.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"You're successfully registered!")
        login_user(user=user)
        return redirect(url_for("homepage"))
    return render_template("register.html", form=form)


@login_manager.user_loader
def load_user(id):
    """
    Retrieve a user object from the database based on the given ID.

    Args:
        id (str): The ID of the user.

    Returns:
        User: The user object associated with the given ID.
    """
    return User.query.get(int(id))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in a user.

    Retrieves the login data from the submitted form, queries the database for the user with the entered username,
    and checks if the entered password matches. If the login is successful, the user is logged in.

    Redirects to the homepage after successful login.

    If the form validation fails or the login is unsuccessful, an error message is flashed, and the login form is rendered.

    Returns:
        Response: A redirect response to the homepage or the login form.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Login Successfully!")
            return redirect(url_for("homepage"))
        else:
            flash("Something went wrong!")
            return redirect(url_for("homepage"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    """
    Log out the current user.

    Logs out the user and redirects to the homepage.

    Returns:
        Response: A redirect response to the homepage.
    """
    logout_user()
    flash(f"You are successfully logged out!")
    return redirect(url_for("homepage"))
