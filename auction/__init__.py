from flask import (
    Flask,
    Blueprint,
    render_template,
    request,
    session,
    url_for,
    redirect,
    flash,
)
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ.setdefault(key, value)

db = SQLAlchemy()


def create_app():
    print(__name__)
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY")
    if not app.secret_key:
        raise ValueError("No SECRET_KEY set - create a .env file")

    # Set app configuration data
    basedir = Path(__file__).parent.parent
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{basedir / 'auction' / 'auction.sqlite'}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    db.init_app(app)
    UPLOAD_FOLDER = "/static/image"
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # Import blueprints and models
    from auction.views import mainbp
    from auction.listings import listingbp
    from auction.auth import authenticationbp
    from auction.models import User

    # Register blueprints
    app.register_blueprint(mainbp)
    app.register_blueprint(listingbp)
    app.register_blueprint(authenticationbp)

    # Initialise bootstrap
    bootstrap = Bootstrap(app)

    # initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = "authentication.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Error handlers
    @app.errorhandler(404)
    def invalid_route(e):
        return render_template("404.html")

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("500.html")

    return app
