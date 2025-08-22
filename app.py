from flask import Flask
from dotenv import load_dotenv
import os
from config import Config
from routes.auth import auth_bp
from routes.main import main_bp
from routes.property import property_bp
from routes.admin import admin_bp
from commands import create_admin as create_admin_command
from routes.admin import admin_bp
from extensions import init_extensions, db
from flask_migrate import Migrate
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
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    init_extensions(app)
    # Initialize Flask-Migrate
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(admin_bp)

    # Register CLI commands
    app.cli.add_command(create_admin_command)

    # Rely on migrations for schema; avoid db.create_all()
    logger.info("App created; use Flask-Migrate for database schema management")

    # Dev-only: allow HTTP OAuth redirects and non-secure session cookies locally
    base_url = app.config.get("BASE_URL", "")
    if base_url.startswith("http://"):
        os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")
        app.config["SESSION_COOKIE_SECURE"] = False
        app.config.setdefault("PREFERRED_URL_SCHEME", "http")

    # Register CLI commands
    app.cli.add_command(create_admin)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
