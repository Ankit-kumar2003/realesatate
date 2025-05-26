import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)
    # Use DATABASE_URL environment variable provided by Render
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///realestate.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-WTF requires a secret key to protect against CSRF attacks
    WTF_CSRF_ENABLED = True
    # Upload folder for property images
    UPLOAD_FOLDER = "static/uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
