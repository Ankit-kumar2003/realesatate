import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)
    # PostgreSQL database URL
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("No DATABASE_URL environment variable set")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-WTF requires a secret key to protect against CSRF attacks
    WTF_CSRF_ENABLED = True
    # Upload folder for property images
    UPLOAD_FOLDER = "static/uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
