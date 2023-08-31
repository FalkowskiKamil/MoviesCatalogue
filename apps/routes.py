from random import choice
from flask import render_template, request
from flask_login import current_user
from apps import app, tmdb_client
from apps.models import User, Post, Rating, PostComment, Favorite
from apps.forms import PostForm, RateForm, CommentForm, FavoriteForm

@app.route("/")
def homepage():
    selected_list = request.args.get("list_type", "popular")
    if selected_list == "today":
        movies = tmdb_client.live()
    else:
        movies = tmdb_client.get_movies(how_many=12, list_type=selected_list)
    return render_template("homepage.html", movies=movies, current_list=selected_list)

@app.route("/search")
def search():
    search_query = request.args.get("search_result", "")
    movies = tmdb_client.search_movie(search_query=search_query)["results"]
    header = f"Result of searching: '{search_query}'"
    return render_template("homepage.html", movies=movies, header=header, search_query=search_query)

@app.route("/favorite/<user_id>")
def favorite(user_id):
    favourite_movies = Favorite.query.filter_by(user_id=user_id, status=True).with_entities(Favorite.movie_id).all()
    favourite_movies= [movie_id for (movie_id,) in favourite_movies]
    movies = list(map(lambda movie_id: tmdb_client.get_single_movie(movie_id), favourite_movies))
    header = f"Favourite Movies of user: '{User.query.filter_by(id=user_id).first().username}':"
    return render_template("homepage.html", movies=movies, header=header)

@app.route("/user/<user_id>")
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(user_id=user.id).order_by(Post.created.desc()).all()
    rating = Rating.query.filter_by(user_id=user.id).order_by(Rating.rate).all()
    if rating:
        mean = [x.rate for x in rating]
        mean = sum(mean) / len(mean)
        mean = round(mean, 2)
        rating = [rating[0], rating[-1], len(rating), mean]

    fav = len(Favorite.query.filter_by(user_id=user_id, status=True).all())
    return render_template("user.html", user=user, post=post, rating=rating, fav=fav)

@app.route("/post/<post_id>", methods=["GET"])
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    comment = PostComment.query.filter_by(post_id=post_id).all()
    form = CommentForm()
    return render_template("post.html", post=post, comment=comment, form=form)

@app.route("/movie_post/<movie_id>/<user_id>")
def movie_post(movie_id, user_id):
    if movie_id == "0":
        head = f"All Post of user: {User.query.filter_by(id=user_id).first().username}"
        posts = Post.query.filter_by(user_id=user_id).all()
    else:
        head = f"All post about movie: {tmdb_client.get_single_movie(movie_id).get('original_title')}"
        posts = Post.query.filter_by(movie_id=movie_id).all()
    return render_template("post_list.html", posts=posts, head=head)

@app.route("/rates/<user_id>")
def all_rates(user_id):
    movies = Rating.query.filter_by(user_id=user_id).order_by(Rating.rate.desc()).all()
    user=User.query.filter_by(id=user_id).first()
    return render_template("rates.html", movies=movies, user=user)

@app.route("/movie/<movie_id>", methods=["GET"])
def movie_details(movie_id):
    forms = {
        "post_form": PostForm(),
        "rate_form": RateForm(),
        "favorite_form": FavoriteForm(),
    }
    tmdb = {
        "movie": tmdb_client.get_single_movie(movie_id),
        "cast": tmdb_client.get_single_movie_cast(movie_id),
    }
    models = {
        "post": Post.query.filter_by(movie_id=movie_id).all(),
        "rate": Rating.query.filter_by(movie_id=movie_id).all(),
    }
    if current_user.is_authenticated:
        models["user_rate"] = Rating.query.filter_by(
            movie_id=movie_id, user_id=current_user.id
        )
    if models["rate"]:
        # Count mean for sum of tmdb and movies catalogue
        rate_in_catalogue = [x.rate for x in models["rate"]]
        mean_catalogue = sum(rate_in_catalogue) / len(rate_in_catalogue)
        sum_rate_value = tmdb["movie"].setdefault("vote_average", 0) * tmdb["movie"].setdefault("vote_count", 0) + mean_catalogue * len(rate_in_catalogue)
        sum_count = tmdb["movie"].setdefault("vote_count", 0)+len(rate_in_catalogue)
        models["mean"] = round(sum_rate_value / sum_count, 2) , sum_count
    else:
        models["mean"] = tmdb["movie"].get("vote_average"), tmdb["movie"].get("vote_count")
    if tmdb["cast"] is not None and len(tmdb["cast"]) > 11:
        tmdb["cast"] = tmdb["cast"][:12]
    if tmdb_client.get_movie_images(movie_id):
        selected_backdrop = choice(tmdb_client.get_movie_images(movie_id))
        models["selected_backdrop"] = selected_backdrop["file_path"]
    return render_template("movie_details.html", tmdb=tmdb, forms=forms, models=models)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)

    def movie_from_id(movie_id):
        return tmdb_client.get_single_movie(movie_id)

    return {"tmdb_image_url": tmdb_image_url, "movie_from_id": movie_from_id}