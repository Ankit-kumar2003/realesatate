from app import create_app
from models.database import db, User
from datetime import datetime


def fix_user_dates():
    app = create_app()
    with app.app_context():
        # Get all users with NULL created_at
        users = User.query.filter(User.created_at.is_(None)).all()

        if not users:
            print("No users found with NULL created_at dates.")
            return

        print(f"Found {len(users)} users with NULL created_at dates.")

        # Update each user
        for user in users:
            user.created_at = datetime.utcnow()
            print(f"Updated user: {user.name} ({user.email})")

        # Commit changes
        db.session.commit()
        print("\nAll users have been updated successfully!")


if __name__ == "__main__":
    fix_user_dates()
