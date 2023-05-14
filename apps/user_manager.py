from flask import redirect, url_for, render_template, flash
from apps import login_manager, app, db
from flask_login import login_required, login_user, logout_user
from apps.forms import RegistrationForm, LoginForm
from apps.models import User

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    # define user with data from form here:
    user = User(username=form.username.data, email=form.email.data)
    # set user's password here:
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash(f'You`re succesfuly registered!')
    login_user(user=user)
    return redirect(url_for('homepage'))
  return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    # query User here:
    user = User.query.filter_by(username=form.username.data).first()
    # check if a user was found and the form password matches here:
    if user and user.check_password(form.password.data):
      # login user here:
      login_user(user, remember=form.remember.data)
      flash(f'Login Succesfuly!')
      return redirect(url_for('homepage'))
    else:
      flash('Something went wrong!')
      return redirect(url_for('homepage'))
  return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'You are succesfuly logout!')
    return redirect(url_for('homepage'))