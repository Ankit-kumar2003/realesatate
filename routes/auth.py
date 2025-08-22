from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db, User
from extensions import oauth
from datetime import datetime
import secrets

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.", "error")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember)
        return redirect(url_for("main.home"))

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email address already exists.", "error")
            return redirect(url_for("auth.register"))

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method="pbkdf2:sha256"),
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@auth_bp.route("/login/google")
def google_login():
    redirect_uri = url_for("auth.google_callback", _external=True)
    nonce = secrets.token_urlsafe(16)
    session["google_oauth_nonce"] = nonce
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)


@auth_bp.route("/auth/google/callback")
def google_callback():
    try:
        # Check if we have the authorization code
        if "code" not in request.args:
            flash("Google authentication was cancelled or failed.", "error")
            return redirect(url_for("auth.login"))

        token = oauth.google.authorize_access_token()
        nonce = session.pop("google_oauth_nonce", None)
        userinfo = oauth.google.parse_id_token(token, nonce=nonce)

        if not userinfo:
            flash("Google authentication failed.", "error")
            return redirect(url_for("auth.login"))

        google_sub = userinfo.get("sub")
        email = userinfo.get("email")
        name = userinfo.get("name") or (userinfo.get("given_name") or "User")
        picture = userinfo.get("picture")

        user = None
        if google_sub:
            user = User.query.filter_by(google_sub=google_sub).first()
        if not user and email:
            user = User.query.filter_by(email=email).first()

        if not user:
            # Create user with a random password (not used for OAuth)
            user = User(
                email=email,
                name=name,
                password=generate_password_hash(secrets.token_urlsafe(16)),
                is_verified=True,
                google_sub=google_sub,
                avatar_url=picture,
                last_login=datetime.utcnow(),
            )
            db.session.add(user)
        else:
            user.google_sub = user.google_sub or google_sub
            user.avatar_url = picture or user.avatar_url
            user.last_login = datetime.utcnow()

        db.session.commit()
        login_user(user, remember=True)
        flash(f"Welcome back, {user.name}!", "success")
        return redirect(url_for("main.home"))

    except Exception as e:
        flash(f"Authentication error: {str(e)}", "error")
        return redirect(url_for("auth.login"))


# @auth_bp.route("/create-admin", methods=["GET", "POST"])
# def create_admin():
#     if request.method == "POST":
#         email = request.form.get("email")
#         name = request.form.get("name")
#         password = request.form.get("password")

#         user = User.query.filter_by(email=email).first()

#         if user:
#             flash("Email address already exists.", "error")
#             return redirect(url_for("auth.create_admin"))

#         new_user = User(
#             email=email,
#             name=name,
#             password=generate_password_hash(password, method="pbkdf2:sha256"),
#             is_admin=True,
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         flash("Admin user created successfully!", "success")
#         return redirect(url_for("auth.login"))

#     return render_template("create_admin.html")
