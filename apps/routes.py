from flask import render_template, request, redirect, flash, url_for
from apps import app, tmdb_client, db, login_manager
from apps.models import User, Post
from apps.forms import RegistrationForm, LoginForm, PostForm
from apps import tmdb_client
from flask_login import login_required, login_user, logout_user, current_user
from random import shuffle
import random
import datetime

FAVORITES=set()

@app.route('/', methods=["GET"])
def homepage():
    movies_list=['now_playing', 'popular', 'top_rated', 'upcoming']
    selected_list=request.args.get('list_type', "popular")
    if selected_list not in movies_list:
        selected_list='popular'
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    shuffle(movies)
    for movie in movies:
        if FAVORITES:
            id=int(movie['id'])
            for x in FAVORITES:
                x=int(x)
                if x==id:
                    movie['fav']='true'
                    break
                else:
                    movie['fav']='false'
        else:
            movie['fav']='false'
    return render_template("homepage.html", movies=movies, current_list=selected_list, movies_list=movies_list)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route("/movie/<movie_id>", methods=['GET', 'POST'])
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    form = PostForm(csrf_enabled=False)
    if request.method == 'POST':  
        if form.validate_on_submit():
            post= Post(
            body = form.body.data,
            user_id = current_user.id,
            movie_id = movie_id
            )
            db.session.add(post)
            db.session.commit()
            flash(f'Succesfully added post!')
    comment=[]
    comment = Post.query.filter_by(movie_id=movie_id).all()
    if cast == None:
        cast = []
    else: 
        cast = tmdb_client.get_single_movie_cast(movie_id)[:10] 
    movie_images = tmdb_client.get_movie_images(movie_id)
    if movie_images == []:
        selected_backdrop = []
    else:
        selected_backdrop = random.choice(movie_images)
        selected_backdrop=selected_backdrop['file_path']
    fav=False
    if movie_id in FAVORITES:
        fav=True
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop, fav=fav, form=form, comment=comment)

@app.route("/search")
def search():
    search_query=request.args.get("q","")
    if search_query:
        response=tmdb_client.search_movie(search_query=search_query)
        if "results" in response:
            movies=response['results']
        else:
            movies=None
    else:
        movies=None
    return render_template("search.html",movies=movies, search_query=search_query)

@app.route("/live")
def live():
    movies=tmdb_client.live()
    today=datetime.date.today()
    return render_template("live.html",movies=movies, today=today)


@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm(csrf_enabled=False)
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
  return render_template('register.html', title='Register', form=form)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm(csrf_enabled=False)
  if form.validate_on_submit():
    # query User here:
    user = User.query.filter_by(email=form.email.data).first()
    # check if a user was found and the form password matches here:
    if user and user.check_password(form.password.data):
      # login user here:
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      flash(f'Login Succesfuly!')
      return redirect(next_page) if next_page else redirect(url_for('homepage'))
    else:
      flash('Something went wrong!')
      return redirect(url_for('homepage'))
  return render_template('login.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  comment = Post.query.filter_by(user_id=user.id).all()
  return render_template('user.html', user=user, comment=comment)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'You are succesfuly logout!')
    return redirect(url_for('homepage'))