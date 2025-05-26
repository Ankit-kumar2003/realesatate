from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.database import db, Property, User, ContactMessage
from functools import wraps

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    total_properties = Property.query.count()
    total_users = User.query.count()
    total_messages = ContactMessage.query.count()
    recent_properties = (
        Property.query.order_by(Property.created_at.desc()).limit(5).all()
    )
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    return render_template(
        "admin/dashboard.html",
        total_properties=total_properties,
        total_users=total_users,
        total_messages=total_messages,
        recent_properties=recent_properties,
        recent_users=recent_users,
    )


@admin_bp.route("/properties")
@login_required
@admin_required
def properties():
    properties = Property.query.order_by(Property.created_at.desc()).all()
    return render_template("admin/properties.html", properties=properties)


@admin_bp.route("/properties/<int:property_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_property(property_id):
    property = Property.query.get_or_404(property_id)
    db.session.delete(property)
    db.session.commit()
    flash("Property deleted successfully.", "success")
    return redirect(url_for("admin.properties"))


@admin_bp.route("/users")
@login_required
@admin_required
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/users/<int:user_id>/toggle-admin", methods=["POST"])
@login_required
@admin_required
def toggle_admin(user_id):
    if user_id == current_user.id:
        flash("You cannot modify your own admin status.", "error")
        return redirect(url_for("admin.users"))

    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(
        f'Admin status {"granted" if user.is_admin else "revoked"} for {user.name}.',
        "success",
    )
    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash("You cannot delete your own account.", "error")
        return redirect(url_for("admin.users"))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/messages")
@login_required
@admin_required
def messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages.html", messages=messages)


@admin_bp.route("/messages/<int:message_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash("Message deleted successfully.", "success")
    return redirect(url_for("admin.messages"))
