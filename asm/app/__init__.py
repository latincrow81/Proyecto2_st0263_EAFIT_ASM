import connexion
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException
from dotenv import dotenv_values

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

    app = connexion.FlaskApp(__name__)
    app.add_api('../openapi.yml')

    # Set app config.
    app.app.config.update(env_config)

    # Set up extensions.
    db.init_app(app.app)
    login_manager.init_app(app.app)

    # Register blueprints.
    app.app.register_blueprint(auth_blueprint)
    app.app.register_blueprint(main_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.anonymous_user = AnonymousUser

    # Error handlers.
    @app.app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template('error.html', error=exc), exc.code
    
    return app
