from datetime import datetime
from flask_login import UserMixin
from apps import db
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index= True, unique = True)
  password_hash = db.Column(db.String(128))
  joined_at = db.Column(db.DateTime(), index = True, default = datetime.utcnow)
  posts = db.relationship("Post", backref="author", lazy="dynamic")
  rate = db.relationship("Rating", backref="reviewer", lazy="dynamic")
  comment = db.relationship("PostComment", backref='commentator', lazy='dynamic')
  
  def __str__(self):
       return f"<User {self.username}>"
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text)
  created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  movie_id = db.Column(db.Integer, index=True)
  comment = db.relationship("PostComment", backref="topic", lazy='dynamic')

  def __str__(self):
      return f"<Post {self.id} {self.body[:50]} ...>"
  
class Rating(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  rate = db.Column(db.Integer, index = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
  movie_id = db.Column(db.Integer, index=True)
  __table_args__ = (UniqueConstraint('user_id', 'movie_id', name='unique_user_movie'),)
  
  def __str__(self):
     return f'<Rate {self.rate}, by {self.user_id}>'
  
class PostComment(db.Model):
  id=db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text)
  created = db.Column(db.DateTime, index= True, default = datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

