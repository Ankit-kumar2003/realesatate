from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
oauth = OAuth()


def init_extensions(app):
    """Initialize Flask extensions with the app"""
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    oauth.init_app(app)

    # Register Google OAuth client if configured
    google_client_id = app.config.get("GOOGLE_CLIENT_ID")
    google_client_secret = app.config.get("GOOGLE_CLIENT_SECRET")
    if google_client_id and google_client_secret:
        oauth.register(
            name="google",
            client_id=google_client_id,
            client_secret=google_client_secret,
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
            client_kwargs={"scope": "openid email profile"},
        )

    # Configure login manager
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    # Register user loader
    from models.database import User  # Import here to avoid circular import

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
