from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.database import db, Property, Contact, User, ContactMessage
from datetime import datetime
from werkzeug.security import generate_password_hash

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def landing():
    featured_properties = (
        Property.query.order_by(Property.created_at.desc()).limit(3).all()
    )
    return render_template("landing.html", properties=featured_properties)


@main_bp.route("/home")
def home():
    # Get search parameters
    location = request.args.get("location", "")
    property_type = request.args.get("property_type", "")
    price_range = request.args.get("price_range", "")

    # Start with base query
    query = Property.query

    # Apply filters
    if location:
        query = query.filter(Property.location.ilike(f"%{location}%"))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if price_range:
        if price_range == "0-100000":
            query = query.filter(Property.price <= 100000)
        elif price_range == "100000-300000":
            query = query.filter(Property.price > 100000, Property.price <= 300000)
        elif price_range == "300000-500000":
            query = query.filter(Property.price > 300000, Property.price <= 500000)
        elif price_range == "500000+":
            query = query.filter(Property.price > 500000)

    # Order by creation date
    properties = query.order_by(Property.created_at.desc()).all()
    return render_template("index.html", properties=properties)


@main_bp.route("/properties")
def properties():
    # Get search parameters
    location = request.args.get("location", "")
    property_type = request.args.get("property_type", "")
    price_range = request.args.get("price_range", "")

    # Start with base query
    query = Property.query

    # Apply filters
    if location:
        query = query.filter(Property.location.ilike(f"%{location}%"))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if price_range:
        if price_range == "0-100000":
            query = query.filter(Property.price <= 100000)
        elif price_range == "100000-300000":
            query = query.filter(Property.price > 100000, Property.price <= 300000)
        elif price_range == "300000-500000":
            query = query.filter(Property.price > 300000, Property.price <= 500000)
        elif price_range == "500000+":
            query = query.filter(Property.price > 500000)

    # Order by creation date
    properties = query.order_by(Property.created_at.desc()).all()
    return render_template("properties.html", properties=properties)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        contact_message = ContactMessage(
            name=name, email=email, subject=subject, message=message
        )
        db.session.add(contact_message)
        db.session.commit()

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html")


@main_bp.route("/property/<int:property_id>")
def property_detail(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template("property_detail.html", property=property)


@main_bp.route("/property/<int:property_id>/contact", methods=["POST"])
def contact_agent(property_id):
    property = Property.query.get_or_404(property_id)

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    message = request.form.get("message")

    contact = Contact(
        name=name,
        email=email,
        subject=f"Property Inquiry: {property.title}",
        message=f"Phone: {phone}\n\nMessage:\n{message}",
    )

    db.session.add(contact)
    db.session.commit()

    flash("Your message has been sent to the agent. They will contact you soon!")
    return redirect(url_for("main.property_detail", property_id=property_id))


@main_bp.route("/add-property", methods=["GET", "POST"])
@login_required
def add_property():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        price = float(request.form.get("price"))
        location = request.form.get("location")
        property_type = request.form.get("property_type")
        bedrooms = int(request.form.get("bedrooms"))
        bathrooms = int(request.form.get("bathrooms"))
        area = float(request.form.get("area"))
        image_url = request.form.get("image_url")

        property = Property(
            title=title,
            description=description,
            price=price,
            location=location,
            property_type=property_type,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area=area,
            image_url=image_url,
            user_id=current_user.id,
        )
        db.session.add(property)
        db.session.commit()
        flash("Property added successfully!", "success")
        return redirect(url_for("main.properties"))
    return render_template("add_property.html")
