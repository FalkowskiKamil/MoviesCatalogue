from flask import render_template, request, flash
from apps import app, tmdb_client
from apps.models import User, Post, Rating, PostComment, Favorite
from apps.forms import  PostForm, RateForm, CommentForm, FavoriteForm
from flask_login import current_user
from random import shuffle
import random
import datetime

@app.route("/")
def homepage():
    selected_list=request.args.get("list_type", "popular")
    # Get a list of movies from the tmdb_client based on the selected list type
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    shuffle(movies) # Shuffle the movies list
    return render_template("homepage.html", movies=movies, current_list=selected_list)

@app.route("/movie/<movie_id>", methods=["GET"])
def movie_details(movie_id):
    # Creates instances of different forms
    forms={
        "post_form": PostForm(),
        "rate_form": RateForm(),
        "favorite_form": FavoriteForm()
    }
    # Retrieves movie information and cast details using the tmdb_client
    tmdb={
        "movie":tmdb_client.get_single_movie(movie_id),
        "cast": tmdb_client.get_single_movie_cast(movie_id),
    }
    # Retrieves related models such as posts and ratings associated with the movie.
    models={
        "post":Post.query.filter_by(movie_id=movie_id).all(),
        "rate":Rating.query.filter_by(movie_id=movie_id).all()
    }
    #  Retrieves the user"s rating for the movie.
    if current_user.is_authenticated:
        models["user_rate"] = Rating.query.filter_by(movie_id=movie_id, user_id = current_user.id)
    # Calculates the mean rating from the retrieved ratings if there are any
    if models["rate"]:
        mean = [x.rate for x in models["rate"]]
        models["mean"] = sum(mean)/len(mean)
    #  Limits the cast details to a maximum of 10 if there are more than 10 cast members.
    if tmdb["cast"] is not None and len(tmdb["cast"]) > 9:
        tmdb["cast"] = tmdb["cast"][:10]        
    # Randomly selects a backdrop image for the movie if available
    if tmdb_client.get_movie_images(movie_id):
        selected_backdrop = random.choice(tmdb_client.get_movie_images(movie_id))
        models["selected_backdrop"] = selected_backdrop["file_path"]
    # Renders the "movie_details.html" template with the retrieved data 
    return render_template("movie_details.html", tmdb=tmdb, forms=forms, models=models)

@app.route("/search")
def search():
    # Retrieve the search query from the request"s query string
    search_query = request.args.get("q", "")
    # Perform a movie search using the search query
    movies = tmdb_client.search_movie(search_query=search_query)["results"]
    # Render the "search.html" template with the search results and search query
    return render_template("search.html", movies=movies, search_query=search_query)


@app.route("/live")
def live():
    # Retrieve a list of currently airing TV shows from the tmdb_client
    movies = tmdb_client.live()
    today = datetime.date.today()
    # Render the "live.html" template with the list of airing shows and today"s date
    return render_template("live.html", movies=movies, today=today)

@app.route("/user/<user_id>")
def user(user_id):
    # Retrieve the user from the database based on the user ID
    user = User.query.filter_by(id=user_id).first_or_404()
    # Retrieve the user"s posts and order them by creation date
    post = Post.query.filter_by(user_id=user.id).order_by(Post.created.desc()).all()
    # If the user has at least one post, retrieve the first post and the total number of posts
    if len(post) > 0:
        post = [post[0], len(post)]
    # Retrieve the user"s ratings and order them by rating value
    rating = Rating.query.filter_by(user_id=user.id).order_by(Rating.rate).all()
    # If the user has at least one rating, calculate the mean rating and retrieve the first rating, last rating, and total number of ratings
    if len(rating) > 0:
        mean = [x.rate for x in rating]
        mean = sum(mean) / len(mean)
        rating = [rating[0], rating[-1], len(rating), mean]
    # Retrieve the number of favorite movies for the user
    fav = len(Favorite.query.filter_by(user_id=user_id, status=True).all())
    # Render the "user.html" template with the user, their posts, ratings, and number of favorite movies
    return render_template("user.html", user=user, post=post, rating=rating, fav=fav)

@app.route("/post/<post_id>", methods=["GET"])
def post(post_id):
    # Retrieve the post from the database based on the post ID
    post = Post.query.filter_by(id=post_id).first()
    # Retrieve the comments for the post
    comment = PostComment.query.filter_by(post_id=post_id).all()
    # Create a CommentForm instance
    form = CommentForm()
    # Render the "post.html" template with the post, comments, and comment form
    return render_template("post.html", post=post, comment=comment, form=form)

@app.route("/movie_post/<movie_id>/<user_id>")
def movie_post(movie_id, user_id):
    # If the movie_id is "0", retrieve all posts by the user
    if movie_id == "0":
        posts = Post.query.filter_by(user_id=user_id).all()
    # Otherwise, retrieve all posts for the specified movie
    else:
        posts = Post.query.filter_by(movie_id=movie_id).all()
    # Render the "movie_post.html" template with the posts
    return render_template("movie_post.html", posts=posts)

@app.route("/favorite/<user_id>")
def favorite(user_id):
    # Retrieve the favorite movies for the specified user_id with status=True
    movies = Favorite.query.filter_by(user_id=user_id, status=True).all()
    return render_template("favorites.html", movies=movies)

@app.route("/rates/<user_id>")
def all_rates(user_id):
    # Retrieve all ratings for the specified user_id
    movies = Rating.query.filter_by(user_id=user_id).order_by(Rating.rate.desc()).all()
    return render_template("rates.html", movies=movies)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
    # Generate the URL for a TMDB poster image using the provided path and size
        return tmdb_client.get_poster_url(path, size)
    def movie_from_id(movie_id):
    # Retrieve detailed information about a movie from its ID using the TMDB API
        return tmdb_client.get_single_movie(movie_id)
    # Define utility functions and variables accessible in templates
    return {"tmdb_image_url": tmdb_image_url, "movie_from_id": movie_from_id}
