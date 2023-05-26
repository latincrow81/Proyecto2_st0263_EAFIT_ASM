import connexion
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from app.grpc_service import run_server
from app.queue_service import init_stats_queue

# instantiate extensions
login_manager = LoginManager()
db = SQLAlchemy()

env_config = dotenv_values(".env")


def create_app():

    from .config import config
    from .views import main_blueprint
    from .auth.views import auth_blueprint
    from .auth.models import User, AnonymousUser

    # Instantiate app.

    app = Flask(__name__)

    # Set app config.
    app.config.update(env_config)

    # Set up extensions.
    db.init_app(app)
    engine = create_engine(env_config.get("SQLALCHEMY_DATABASE_URI"))
    if not database_exists(engine.url):
        create_database(engine.url)
    login_manager.init_app(app)

    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.anonymous_user = AnonymousUser

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template('error.html', error=exc), exc.code

    init_stats_queue()
    run_server()
    return app
