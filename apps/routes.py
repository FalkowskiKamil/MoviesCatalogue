from flask import render_template, request
from apps import app, tmdb_client
from apps.models import User, Post, Rating, PostComment, Favorite
from apps.forms import PostForm, RateForm, CommentForm, FavoriteForm
from flask_login import current_user
from random import shuffle
import random
import datetime


@app.route("/")
def homepage():
    """
    Renders the homepage template with a list of movies based on the selected list type.

    The list type can be provided as a query parameter "list_type" in the request.
    The movies are retrieved from the tmdb_client based on the selected list type.
    The movies list is shuffled before rendering.

    Returns:
        The rendered homepage.html template with the movies and current_list.
    """
    selected_list = request.args.get("list_type", "popular")
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    shuffle(movies)
    return render_template("homepage.html", movies=movies, current_list=selected_list)


@app.route("/movie/<movie_id>", methods=["GET"])
def movie_details(movie_id):
    """
    Renders the movie_details template with movie information, cast details, related posts, and ratings.

    Args:
        movie_id (str): The ID of the movie to retrieve details for.

    Returns:
        The rendered movie_details.html template with the retrieved data.
    """
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
        mean = [x.rate for x in models["rate"]]
        models["mean"] = sum(mean) / len(mean)
    if tmdb["cast"] is not None and len(tmdb["cast"]) > 11:
        tmdb["cast"] = tmdb["cast"][:12]
    if tmdb_client.get_movie_images(movie_id):
        selected_backdrop = random.choice(tmdb_client.get_movie_images(movie_id))
        models["selected_backdrop"] = selected_backdrop["file_path"]
    return render_template("movie_details.html", tmdb=tmdb, forms=forms, models=models)


@app.route("/search")
def search():
    """
    Performs a movie search based on the provided search query.

    The search query is retrieved from the request's query string parameter "query".
    The movies matching the search query are retrieved from tmdb_client.

    Returns:
        The rendered search.html template with the search results and search_query.
    """
    search_query = request.args.get("q", "")
    movies = tmdb_client.search_movie(search_query=search_query)["results"]
    return render_template("search.html", movies=movies, search_query=search_query)


@app.route("/live")
def live():
    """
    Retrieves a list of currently airing TV shows from the tmdb_client.
    Renders the "live.html" template with the list of airing shows and today's date.

    Returns:
        The rendered live.html template with the list of airing shows and today's date.
    """
    movies = tmdb_client.live()
    today = datetime.date.today()
    return render_template("live.html", movies=movies, today=today)


@app.route("/user/<user_id>")
def user(user_id):
    """
    Retrieves a user from the database based on the user ID.
    Retrieves the user's posts, ratings, and number of favorite movies.
    Renders the "user.html" template with the user, their posts, ratings, and number of favorite movies.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        The rendered user.html template with the user, their posts, ratings, and number of favorite movies.
    """
    user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(user_id=user.id).order_by(Post.created.desc()).all()
    if len(post) > 0:
        post = [post[0], len(post)]
    rating = Rating.query.filter_by(user_id=user.id).order_by(Rating.rate).all()
    if len(rating) > 0:
        mean = [x.rate for x in rating]
        mean = sum(mean) / len(mean)
        rating = [rating[0], rating[-1], len(rating), mean]
    fav = len(Favorite.query.filter_by(user_id=user_id, status=True).all())
    return render_template("user.html", user=user, post=post, rating=rating, fav=fav)


@app.route("/post/<post_id>", methods=["GET"])
def post(post_id):
    """
    Retrieves a post from the database based on the post ID.
    Retrieves the comments for the post.
    Creates a CommentForm instance.
    Renders the "post.html" template with the post, comments, and comment form.

    Args:
        post_id (str): The ID of the post to retrieve.

    Returns:
        The rendered post.html template with the post, comments, and comment form.
    """
    post = Post.query.filter_by(id=post_id).first()
    comment = PostComment.query.filter_by(post_id=post_id).all()
    form = CommentForm()
    return render_template("post.html", post=post, comment=comment, form=form)


@app.route("/movie_post/<movie_id>/<user_id>")
def movie_post(movie_id, user_id):
    """
    Retrieves posts related to a specific movie or user.
    Renders the "movie_post.html" template with the posts.

    Args:
        movie_id (str): The ID of the movie. If "0", retrieve all posts by the user.
        user_id (str): The ID of the user.

    Returns:
        The rendered movie_post.html template with the posts.
    """
    if movie_id == "0":
        posts = Post.query.filter_by(user_id=user_id).all()
    else:
        posts = Post.query.filter_by(movie_id=movie_id).all()
    return render_template("movie_post.html", posts=posts)


@app.route("/favorite/<user_id>")
def favorite(user_id):
    """
    Retrieves the favorite movies for a specified user.
    Renders the "favorites.html" template with the favorite movies.

    Args:
        user_id (str): The ID of the user.

    Returns:
        The rendered favorites.html template with the favorite movies.
    """
    movies = Favorite.query.filter_by(user_id=user_id, status=True).all()
    return render_template("favorites.html", movies=movies)


@app.route("/rates/<user_id>")
def all_rates(user_id):
    """
    Retrieves all ratings for a specified user.
    Renders the "rates.html" template with the ratings.

    Args:
        user_id (str): The ID of the user.

    Returns:
        The rendered rates.html template with the ratings.
    """
    movies = Rating.query.filter_by(user_id=user_id).order_by(Rating.rate.desc()).all()
    return render_template("rates.html", movies=movies)


@app.context_processor
def utility_processor():
    """
    Defines utility functions and variables accessible in templates.
    Provides functions for generating TMDB image URLs and retrieving detailed movie information from TMDB.

    Returns:
        A dictionary containing the utility functions and variables accessible in templates.
    """

    def tmdb_image_url(path, size):
        """
        Generates the URL for a TMDB poster image using the provided path and size.

        Args:
            path (str): The path of the image.
            size (str): The desired size of the image.

        Returns:
            The URL of the TMDB poster image.
        """
        return tmdb_client.get_poster_url(path, size)

    def movie_from_id(movie_id):
        """
        Retrieves detailed information about a movie from its ID using the TMDB API.

        Args:
            movie_id (str): The ID of the movie.

        Returns:
            The detailed information about the movie.
        """
        return tmdb_client.get_single_movie(movie_id)

    return {"tmdb_image_url": tmdb_image_url, "movie_from_id": movie_from_id}
