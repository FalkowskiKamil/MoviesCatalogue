from flask import redirect, url_for, render_template, flash
from apps import login_manager, app, db
from flask_login import login_required, login_user, logout_user
from apps.forms import RegistrationForm, LoginForm
from apps.models import User

@app.route("/register", methods=["GET", "POST"])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    # Create a new user object with data from the form
    user = User(username=form.username.data, email=form.email.data)
    # Set the user"s password
    user.set_password(form.password.data)
    # Add the user to the database
    db.session.add(user)
    db.session.commit()
    flash(f"You`re succesfully registered!")
    # Log in the newly registered user
    login_user(user=user)
    return redirect(url_for("homepage"))
  return render_template("register.html", form=form)

@login_manager.user_loader
def load_user(id):
    # Load the user from the database based on the given id
    return User.query.get(int(id))

@app.route("/login", methods=["GET","POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    # Query the database for the user with the entered username
    user = User.query.filter_by(username=form.username.data).first()
    # Check if a user was found and if the entered password matches
    if user and user.check_password(form.password.data):
      # Log in the user
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
    # Log out the current user
    logout_user()
    flash(f"You are successfully logged out!")
    return redirect(url_for("homepage"))