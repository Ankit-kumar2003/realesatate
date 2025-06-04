from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import getpass
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import text

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.urandom(24)

# Initialize database
db = SQLAlchemy(app)


# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def create_admin():
    with app.app_context():
        try:
            # Drop all tables with CASCADE
            db.session.execute(text('DROP SCHEMA public CASCADE;'))
            db.session.execute(text('CREATE SCHEMA public;'))
            db.session.commit()
            
            # Create all tables
            db.create_all()

            print("\nCreate New Admin User")
            print("----------------------")
            name = input("Enter admin name: ")
            email = input("Enter admin email: ")

            # Check if email already exists
            if User.query.filter_by(email=email).first():
                print("Error: A user with this email already exists!")
                return

            # Get password securely
            while True:
                password = getpass.getpass("Enter admin password: ")
                confirm_password = getpass.getpass("Confirm password: ")
                if password == confirm_password:
                    break
                print("Passwords do not match. Please try again.")

            # Create new admin user
            admin = User(
                name=name,
                email=email,
                password=generate_password_hash(password),
                is_admin=True,
            )

            # Add to database
            db.session.add(admin)
            db.session.commit()
            print(f"\nAdmin user '{name}' created successfully!")
            print(f"Email: {email}")
            
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {str(e)}")
            raise


def list_admins():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        admins = User.query.filter_by(is_admin=True).all()
        if not admins:
            print("No admin users found.")
            return

        print("\nExisting Admin Users:")
        print("-------------------")
        for admin in admins:
            print(f"Name: {admin.name}")
            print(f"Email: {admin.email}")
            print("-------------------")


if __name__ == "__main__":
    print("\nAdmin Management")
    print("---------------")
    print("1. List all admins")
    print("2. Add a new admin")
    choice = input("\nEnter your choice (1 or 2): ")

    if choice == "1":
        list_admins()
    elif choice == "2":
        create_admin()
    else:
        print("Invalid choice.")
