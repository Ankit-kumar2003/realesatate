import click
from flask.cli import with_appcontext
from models.database import db, User
from werkzeug.security import generate_password_hash


@click.command("create-admin")
@click.argument("email")
@click.argument("password")
@click.argument("name")
@with_appcontext
def create_admin(email, password, name):
    """Create an admin user."""
    try:
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            click.echo("Error: User with this email already exists.")
            return

        # Create new admin user
        admin = User(
            email=email,
            password=generate_password_hash(password),
            name=name,
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()
        click.echo(f"Successfully created admin user: {email}")
    except Exception as e:
        click.echo(f"Error creating admin user: {str(e)}")
        db.session.rollback()
