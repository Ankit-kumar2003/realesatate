from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.database import db, Property, Contact, User, ContactMessage, PropertyViewing
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
    now = datetime.now()
    return render_template("property_detail.html", property=property, now=now)


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

    flash(
        "Your message has been sent to the property owner. They will contact you soon!",
        "success",
    )
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


@main_bp.route("/property/<int:property_id>/schedule-viewing", methods=["POST"])
def schedule_viewing(property_id):
    property = Property.query.get_or_404(property_id)

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    preferred_date = datetime.strptime(
        request.form.get("preferred_date"), "%Y-%m-%d"
    ).date()
    preferred_time = request.form.get("preferred_time")
    message = request.form.get("message", "")

    viewing = PropertyViewing(
        property_id=property_id,
        name=name,
        email=email,
        phone=phone,
        preferred_date=preferred_date,
        preferred_time=preferred_time,
        message=message,
    )

    db.session.add(viewing)
    db.session.commit()

    flash(
        "Your viewing request has been submitted. The property owner will contact you soon!",
        "success",
    )
    return redirect(url_for("main.property_detail", property_id=property_id))


@main_bp.route("/dashboard")
@login_required
def user_dashboard():
    # Get user's properties
    properties = (
        Property.query.filter_by(user_id=current_user.id)
        .order_by(Property.created_at.desc())
        .all()
    )

    # Get viewing requests for user's properties
    property_ids = [p.id for p in properties]
    viewings = (
        PropertyViewing.query.filter(PropertyViewing.property_id.in_(property_ids))
        .order_by(PropertyViewing.created_at.desc())
        .all()
    )

    # Get messages only for user's properties
    property_titles = [p.title for p in properties]
    messages = Contact.query.filter(Contact.subject.like("Property Inquiry:%")).all()

    # Filter messages to only include those for user's properties
    user_messages = []
    for message in messages:
        property_title = message.subject.split(": ")[1]
        if property_title in property_titles:
            user_messages.append(message)

    return render_template(
        "user/dashboard.html",
        properties=properties,
        viewings=viewings,
        messages=user_messages,
    )


@main_bp.route("/property/<int:property_id>/edit", methods=["GET", "POST"])
@login_required
def edit_property(property_id):
    property = Property.query.get_or_404(property_id)

    # Check if user owns the property
    if property.user_id != current_user.id:
        flash("You don't have permission to edit this property.", "error")
        return redirect(url_for("main.property_detail", property_id=property_id))

    if request.method == "POST":
        property.title = request.form.get("title")
        property.description = request.form.get("description")
        property.price = float(request.form.get("price"))
        property.location = request.form.get("location")
        property.property_type = request.form.get("property_type")
        property.bedrooms = int(request.form.get("bedrooms"))
        property.bathrooms = int(request.form.get("bathrooms"))
        property.area = float(request.form.get("area"))
        property.image_url = request.form.get("image_url")

        db.session.commit()
        flash("Property updated successfully!", "success")
        return redirect(url_for("main.user_dashboard"))

    return render_template("edit_property.html", property=property)


@main_bp.route("/property/<int:property_id>/delete", methods=["POST"])
@login_required
def delete_property(property_id):
    property = Property.query.get_or_404(property_id)

    # Check if user owns the property
    if property.user_id != current_user.id:
        flash("You don't have permission to delete this property.", "error")
        return redirect(url_for("main.property_detail", property_id=property_id))

    db.session.delete(property)
    db.session.commit()
    flash("Property deleted successfully!", "success")
    return redirect(url_for("main.user_dashboard"))


@main_bp.route("/viewing/<int:viewing_id>/approve", methods=["POST"])
@login_required
def approve_viewing(viewing_id):
    viewing = PropertyViewing.query.get_or_404(viewing_id)
    property = Property.query.get_or_404(viewing.property_id)

    # Check if user owns the property
    if property.user_id != current_user.id:
        flash("You don't have permission to manage this viewing request.", "error")
        return redirect(url_for("main.user_dashboard"))

    viewing.status = "approved"
    db.session.commit()
    flash("Viewing request approved!", "success")
    return redirect(url_for("main.user_dashboard"))


@main_bp.route("/viewing/<int:viewing_id>/reject", methods=["POST"])
@login_required
def reject_viewing(viewing_id):
    viewing = PropertyViewing.query.get_or_404(viewing_id)
    property = Property.query.get_or_404(viewing.property_id)

    # Check if user owns the property
    if property.user_id != current_user.id:
        flash("You don't have permission to manage this viewing request.", "error")
        return redirect(url_for("main.user_dashboard"))

    viewing.status = "rejected"
    db.session.commit()
    flash("Viewing request rejected!", "success")
    return redirect(url_for("main.user_dashboard"))


@main_bp.route("/message/<int:message_id>/delete", methods=["POST"])
@login_required
def delete_message(message_id):
    message = Contact.query.get_or_404(message_id)

    # Extract property title from message subject
    try:
        property_title = message.subject.split(": ")[1]
        property = Property.query.filter_by(
            title=property_title, user_id=current_user.id
        ).first()

        if not property:
            flash("You don't have permission to delete this message.", "error")
            return redirect(url_for("main.user_dashboard"))

        db.session.delete(message)
        db.session.commit()
        flash("Message deleted successfully!", "success")
    except:
        flash("Invalid message format.", "error")

    return redirect(url_for("main.user_dashboard"))
