from flask import flash, redirect, url_for, request
from apps import app, db
from apps.forms import PostForm, RateForm, CommentForm, FavoriteForm
from apps.models import Post, Rating, PostComment, Favorite
from flask_login import current_user


@app.route("/post/<post_id>/comment", methods=["POST"])
def add_comment(post_id):
    """
    Add a comment to a post.

    Retrieves the comment data from the submitted form, creates a new `PostComment` object,
    associates it with the current user and the specified post, and saves it to the database.

    Redirects back to the post details page after adding the comment.

    If the form validation fails, no action is taken.

    Args:
        post_id (int): The ID of the post.

    Returns:
        Response: A redirect response back to the post details page.
    """
    form = CommentForm()
    if form.validate_on_submit():
        comment_add = PostComment(
            body=form.body.data, user_id=current_user.id, post_id=post_id
        )
        db.session.add(comment_add)
        db.session.commit()
        flash("Successfully added comment!")
    return redirect(url_for("post", post_id=post_id))


@app.route("/movie/<movie_id>/post", methods=["POST"])
def add_post(movie_id):
    """
    Add a new post for a movie.

    Retrieves the post data from the submitted form, creates a new `Post` object,
    associates it with the current user and the specified movie, and saves it to the database.

    Redirects back to the movie details page after adding the post.

    If the form validation fails, no action is taken.

    Args:
        movie_id (int): The ID of the movie.

    Returns:
        Response: A redirect response back to the movie details page.
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, user_id=current_user.id, movie_id=movie_id)
        db.session.add(post)
        db.session.commit()
        flash(f"Succesfully added post!")
    return redirect(url_for("movie_details", movie_id=movie_id))


@app.route("/movie/<movie_id>/rate", methods=["POST"])
def add_rate(movie_id):
    """
    Add or update a user's rating for a movie.

    Retrieves the rating data from the submitted form. If the user has already rated the movie,
    the existing rating is updated; otherwise, a new `Rating` object is created.

    Redirects back to the movie details page after adding or updating the rating.

    If the form validation fails, no action is taken.

    Args:
        movie_id (int): The ID of the movie.

    Returns:
        Response: A redirect response back to the movie details page.
    """
    form = RateForm()
    if form.validate_on_submit():
        existing_rating = Rating.query.filter_by(
            movie_id=movie_id, user_id=current_user.id
        ).first()
        if existing_rating:
            # Update the user's existing rating
            existing_rating.rate = form.rate.data
            flash("Your rating has been updated!", "success")
        else:
            # Create a new rating for the user
            rating = Rating(
                rate=form.rate.data, user_id=current_user.id, movie_id=movie_id
            )
            db.session.add(rating)
            flash(f"Successfully added rate!")
        db.session.commit()
    return redirect(url_for("movie_details", movie_id=movie_id))


@app.route("/movie/<movie_id>/favorite", methods=["POST"])
def add_favorite(movie_id):
    """
    Add or remove a movie from a user's favorites.

    Checks if the movie is already in the user's favorites. If it is, the movie is removed;
    otherwise, it is added. The favorite status is toggled accordingly.

    Redirects back to the previous page after adding or removing the favorite.

    If no referrer URL is available, it redirects to the movie details page.

    Args:
        movie_id (int): The ID of the movie.

    Returns:
        Response: A redirect response back to the previous page or the movie details page.
    """
    form = FavoriteForm()
    if form.validate_on_submit():
        favorite = Favorite.query.filter_by(
            movie_id=movie_id, user_id=current_user.id
        ).first()
        if favorite is None:
            favorite = Favorite(movie_id=movie_id, user_id=current_user.id, status=True)
            db.session.add(favorite)
            flash(f"Movie added to favorite!")
        else:
            # Toggle the existing favorite status
            favorite.status = not favorite.status
            if favorite.status == True:
                status = "added to"
            else:
                status = "removed from"
            flash(f"Movie {status} favorite!")
        db.session.commit()
    referrer = request.referrer
    if referrer is None:
        # If no referrer URL is available, redirect to the movie details page
        return redirect(url_for("movie_details", movie_id=movie_id))
    else:
        return redirect(referrer)
