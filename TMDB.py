from apps import app, db

from apps.models import User, Post
from apps import routes, models, forms, user_manager, data_manager, tmdb_client, test_tmdb_client
@app.shell_context_processor
def make_shell_context():
   return {
       "db": db,
       "User": User,
       "Post": Post,
   }