from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config.config import Config
from routes.auth import auth_bp
from routes.main import main_bp
from routes.admin import admin_bp
from models.database import db, User
from commands import create_admin
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

# Create a logger
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    # Register CLI commands
    app.cli.add_command(create_admin)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Log database connection events
    @app.before_request
    def before_request():
        logger.info("Connecting to database...")

    @app.after_request
    def after_request(response):
        logger.info("Database connection closed.")
        return response

    return app


# Create the Flask application instance at the module level
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
