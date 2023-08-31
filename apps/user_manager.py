from flask import redirect, url_for, render_template, flash
from flask_login import login_required, login_user, logout_user
from apps import login_manager, app, db
from apps.forms import RegistrationForm, LoginForm
from apps.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f"Login Successfully!")
            return redirect(url_for("homepage"))
        else:
            flash("Something went wrong!")
            return redirect(url_for("homepage"))
    return render_template("register_login_form.html", form=form, login=True)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"You're successfully registered!")
        login_user(user=user)
        return redirect(url_for("homepage"))
    return render_template("register_login_form.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f"You are successfully logged out!")
    return redirect(url_for("homepage"))