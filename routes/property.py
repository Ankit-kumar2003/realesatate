from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.database import db, Property
from datetime import datetime

property_bp = Blueprint("property", __name__)


@property_bp.route("/properties")
def list_properties():
    properties = Property.query.all()
    return render_template("property/list.html", properties=properties)


@property_bp.route("/property/<int:property_id>")
def view_property(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template("property/view.html", property=property)


@property_bp.route("/property/add", methods=["GET", "POST"])
@login_required
def add_property():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        price = request.form.get("price")
        location = request.form.get("location")
        property_type = request.form.get("type")

        new_property = Property(
            title=title,
            description=description,
            price=price,
            location=location,
            type=property_type,
            user_id=current_user.id,
            created_at=datetime.utcnow(),
        )

        db.session.add(new_property)
        db.session.commit()

        flash("Property added successfully!", "success")
        return redirect(url_for("property.view_property", property_id=new_property.id))

    return render_template("property/add.html")


@property_bp.route("/property/<int:property_id>/edit", methods=["GET", "POST"])
@login_required
def edit_property(property_id):
    property = Property.query.get_or_404(property_id)

    if property.user_id != current_user.id:
        flash("You don't have permission to edit this property.", "error")
        return redirect(url_for("property.view_property", property_id=property_id))

    if request.method == "POST":
        property.title = request.form.get("title")
        property.description = request.form.get("description")
        property.price = request.form.get("price")
        property.location = request.form.get("location")
        property.type = request.form.get("type")

        db.session.commit()
        flash("Property updated successfully!", "success")
        return redirect(url_for("property.view_property", property_id=property_id))

    return render_template("property/edit.html", property=property)


@property_bp.route("/property/<int:property_id>/delete", methods=["POST"])
@login_required
def delete_property(property_id):
    property = Property.query.get_or_404(property_id)

    if property.user_id != current_user.id:
        flash("You don't have permission to delete this property.", "error")
        return redirect(url_for("property.view_property", property_id=property_id))

    db.session.delete(property)
    db.session.commit()

    flash("Property deleted successfully!", "success")
    return redirect(url_for("property.list_properties"))
