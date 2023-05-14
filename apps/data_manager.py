from flask import flash, redirect, url_for, request
from apps import app, db
from apps.forms import  PostForm, RateForm, CommentForm, FavoriteForm
from apps.models import Post, Rating, PostComment, Favorite
from flask_login import current_user


@app.route('/post/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment_add = PostComment(
            body=form.body.data,
            user_id=current_user.id,
            post_id=post_id
        )
        db.session.add(comment_add)
        db.session.commit()
        flash('Successfully added comment!')
    return redirect(url_for('post', post_id=post_id))

@app.route('/movie/<movie_id>/post', methods=['POST'])
def add_post(movie_id):
    form=PostForm()
    if form.validate_on_submit():
        post= Post(
        body = form.body.data,
        user_id = current_user.id,
        movie_id = movie_id
        )
        db.session.add(post)
        db.session.commit()
        flash(f'Succesfully added post!')
    return redirect(url_for('movie_details', movie_id=movie_id))


@app.route('/movie/<movie_id>/rate', methods=['POST'])
def add_rate(movie_id):
    form=RateForm()
    if form.validate_on_submit():
        existing_rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
        if existing_rating:
            # Update the user's existing rating
            existing_rating.rate = form.rate.data
            flash('Your rating has been updated!', 'success')
        else:
            # Create a new rating for the user
            rating = Rating(
                rate=form.rate.data,
                user_id=current_user.id,
                movie_id=movie_id
            )
            db.session.add(rating)
            
            flash(f'Successfully added rate!')
        db.session.commit()
    return redirect(url_for('movie_details', movie_id=movie_id))

@app.route('/movie/<movie_id>/favorite', methods=['POST'])
def add_favorite(movie_id):
    form=FavoriteForm()
    if form.validate_on_submit():
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
    referrer = request.referrer
    if referrer is None:
        # If no referrer URL is available, redirect to the movie details page
        return redirect(url_for('movie_details', movie_id=movie_id))
    else:
        return redirect(referrer)