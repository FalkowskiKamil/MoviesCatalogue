from flask import render_template, request, redirect, flash, url_for
from apps import app, tmdb_client, db, login_manager
from apps.models import User, Post, Rating, PostComment, Favorite
from apps.forms import RegistrationForm, LoginForm, PostForm, RateForm, CommentForm, FavoriteForm
from apps import tmdb_client
from flask_login import login_required, login_user, logout_user, current_user
from random import shuffle
import random
import datetime

@app.route('/', methods=["GET"])
def homepage():
    movies_list=['now_playing', 'popular', 'top_rated', 'upcoming']
    selected_list=request.args.get('list_type', "popular")
    if selected_list not in movies_list:
        selected_list='popular'
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    shuffle(movies)
    return render_template("homepage.html", movies=movies, current_list=selected_list, movies_list=movies_list)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    def title_from_id(movie_id):
        return tmdb_client.get_single_movie(movie_id)['original_title']
    return {"tmdb_image_url": tmdb_image_url, "tittle_from_id": title_from_id}

@app.route("/movie/<movie_id>", methods=['GET', 'POST'])
def movie_details(movie_id):
    cast,user_rate,mean,rate,comment, selected_backdrop =[[] for _ in range(6)]
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    form = PostForm(csrf_enabled=False)
    form2 = RateForm(csrf_enabled=False)
    favorite_form = FavoriteForm(csr_enabled=False)
    if request.method == 'POST':  
        if 'rate' in request.form:
            if form2.validate_on_submit():
                existing_rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
                if existing_rating:
                    # Update the user's existing rating
                    existing_rating.rate = form2.rate.data
                    try:
                        db.session.commit()
                        flash('Your rating has been updated!', 'success')
                    except Exception as e:
                        print('Error committing rating update:', e)
                        db.session.rollback()
                        flash('There was an error updating your rating. Please try again later.', 'danger')
                else:
                    # Create a new rating for the user
                    rating = Rating(
                        rate=form2.rate.data,
                        user_id=current_user.id,
                        movie_id=movie_id
                    )
                    db.session.add(rating)
                    db.session.commit()
                    flash(f'Successfully added rate!')
        elif 'favorite' in request.form:
            if favorite_form.validate_on_submit():
                favorite = Favorite.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
                if favorite is None:
                    favorite = Favorite(movie_id=movie_id, user_id=current_user.id, status=True)
                    db.session.add(favorite)
                    flash(f'Movie added to favorite!')
                else:
                    # Toggle the existing favorite status
                    favorite.status = not favorite.status
                    flash(f'Movie {favorite.status} in favorite!')
                db.session.commit()
        else:
            if form.validate_on_submit():
                post= Post(
                body = form.body.data,
                user_id = current_user.id,
                movie_id = movie_id
                )
                db.session.add(post)
                db.session.commit()
                flash(f'Succesfully added post!')
    comment = Post.query.filter_by(movie_id=movie_id).all()
    rate = Rating.query.filter_by(movie_id=movie_id).all()
    if current_user.is_authenticated:
        user_rate = Rating.query.filter_by(movie_id=movie_id, user_id = current_user.id)
    if rate:
        mean = [x.rate for x in rate]
        mean = sum(mean)/len(mean)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    if cast is not None and len(cast) > 0:
        cast = cast[:min(10, len(cast))]        
    movie_images = tmdb_client.get_movie_images(movie_id)
    if movie_images != []:
        selected_backdrop = random.choice(movie_images)
        selected_backdrop=selected_backdrop['file_path']
    return render_template("movie_details.html",mean=mean, movie=details, rate = rate, user_rate=user_rate, cast=cast, selected_backdrop=selected_backdrop, form=form, form2 = form2,favorite_form=favorite_form, comment=comment)

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
    user = User.query.filter_by(username=form.username.data).first()
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
  rates = Rating.query.filter_by(user_id=user.id).all()
  fav = Favorite.query.filter_by(user_id=user.id).all()
  return render_template('user.html', user=user, comment=comment, rates=rates, fav=fav)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(f'You are succesfuly logout!')
    return redirect(url_for('homepage'))

@app.route('/post/<post_id>',  methods=['GET', 'POST'])
def post(post_id):
    post= Post.query.filter_by(id=post_id).first()
    form = CommentForm(csrf_enabled=False)
    if request.method == 'POST':  
        if form.validate_on_submit():
            comment_add = PostComment(
                body = form.body.data,
                user_id = current_user.id,
                post_id = post_id
            )
            db.session.add(comment_add)
            db.session.commit()
            flash(f'Succesfully added comment!')
    comment = PostComment.query.filter_by(post_id=post_id).all()
    return render_template("post.html", post=post, comment=comment, form=form)

@app.route('/movie_post/<movie_id>')
def movie_post(movie_id):
    post= Post.query.filter_by(movie_id=movie_id).all()   
    return render_template("movie_post.html", post=post)