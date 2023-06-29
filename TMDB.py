from apps import app, db

from apps.models import User, Post
from apps import (
    routes,
    models,
    forms,
    user_manager,
    data_manager,
    tmdb_client,
    test_tmdb_client,
)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
