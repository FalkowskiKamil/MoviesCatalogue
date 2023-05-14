from flask import render_template, request
from apps import app, tmdb_client
from apps.models import User, Post, Rating, PostComment, Favorite
from apps.forms import  PostForm, RateForm, CommentForm, FavoriteForm
from flask_login import current_user
from random import shuffle
import random
import datetime

@app.route('/')
def homepage():
    selected_list=request.args.get('list_type', "popular")
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    shuffle(movies)
    return render_template("homepage.html", movies=movies, current_list=selected_list)

@app.route("/movie/<movie_id>", methods=['GET'])
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    postform = PostForm(csrf_enabled=False)
    rate_form = RateForm(csrf_enabled=False)
    favorite_form = FavoriteForm(csr_enabled=False)
    comment = Post.query.filter_by(movie_id=movie_id).all()
    rate = Rating.query.filter_by(movie_id=movie_id).all()
    if current_user.is_authenticated:
        user_rate = Rating.query.filter_by(movie_id=movie_id, user_id = current_user.id)
    mean,selected_backdrop=[],[]
    if rate:
        mean = [x.rate for x in rate]
        mean = sum(mean)/len(mean)
    if cast is not None and len(cast) > 9:
        cast = cast[:10]        
    movie_images = tmdb_client.get_movie_images(movie_id)
    if movie_images != []:
        selected_backdrop = random.choice(movie_images)
        selected_backdrop=selected_backdrop['file_path']
    return render_template("movie_details.html",mean=mean, movie=details, rate = rate, user_rate=user_rate, cast=cast, selected_backdrop=selected_backdrop, postform=postform, rate_form = rate_form,favorite_form=favorite_form, comment=comment)

@app.route("/search")
def search():
    search_query=request.args.get("q","")
    movies=tmdb_client.search_movie(search_query=search_query)['results']
    return render_template("search.html",movies=movies, search_query=search_query)

@app.route("/live")
def live():
    movies=tmdb_client.live()
    today=datetime.date.today()
    return render_template("live.html",movies=movies, today=today)

@app.route('/user/<username>')
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  comment= Post.query.filter_by(user_id=user.id).order_by(Post.created.desc()).all()
  if comment != None:
    comment = [comment[0], len(comment)]
  rating = Rating.query.filter_by(user_id=user.id).order_by(Rating.rate).all()
  if rating != None:
    mean = [x.rate for x in rating]
    mean = sum(mean)/len(mean)
    rating = [rating[0], rating[-1], len(rating), mean]
  fav = len(Favorite.query.filter_by(user_id=user.id, status=True).all())
  return render_template('user.html', user=user, comment=comment, rating=rating, fav=fav)

@app.route('/post/<post_id>', methods=['GET'])
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    comment = PostComment.query.filter_by(post_id=post_id).all()
    form = CommentForm()
    return render_template("post.html", post=post, comment=comment, form=form)


@app.route('/movie_post/<movie_id>/<user_id>')
def movie_post(movie_id, user_id):
    if movie_id=='0':
        post= Post.query.filter_by(user_id=user_id).all()
    else:
        post= Post.query.filter_by(movie_id=movie_id).all()
    return render_template("movie_post.html", post=post)

@app.route('/favorite/<user_id>')
def favorite(user_id):
    movies = Favorite.query.filter_by(user_id=user_id, status=True).all()
    return render_template('favorites.html', movies=movies)

@app.route('/rates/<user_id>')
def all_rates(user_id):
    movies = Rating.query.filter_by(user_id=user_id).all()
    return render_template('rates.html', movies=movies)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    def movie_from_id(movie_id):
        return tmdb_client.get_single_movie(movie_id)
    return {"tmdb_image_url": tmdb_image_url, "movie_from_id": movie_from_id}
