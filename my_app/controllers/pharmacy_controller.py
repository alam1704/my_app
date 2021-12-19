from flask import Blueprint, request, render_template, redirect, url_for, abort, flash
from main import db, lm
from models.pharmacies import Pharmacy
from models.staffs import Staff
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError
from schemas.pharmacy_schema import pharmacies_schema, pharmacy_schema, pharmacy_update_schema
from schemas.staff_schema import staffs_schema, staff_schema


@lm.user_loader
def load_user(pharmacy):
    return Pharmacy.query.get(pharmacy)

@lm.unauthorized_handler
def unauthorized():
    return redirect("/login/")

pharmacies = Blueprint('pharmacies', __name__)
# Now register this new controller by adding it into the __init__.py file

@pharmacies.route('/pharmacies/', methods=["GET"])
def get_pharmacies():
    data = {
        "page_title": "Pharmacies Index",
        "pharmacies": pharmacies_schema.dump(Pharmacy.query.all())
    }
    return render_template("pharmacies_index.html", page_data=data)

@pharmacies.route('/pharmacies/account/', methods=["GET", "POST"])
@login_required
def get_pharmacy_member():
    staff = Staff.query.order_by(Staff.staff_name).filter_by(creator_id=current_user.pharmacy_id)
    if request.method == "GET":
        data = {
            "page_title":"Your Account details",
            "staffs" : staffs_schema.dump(staff)
        }
        return render_template("pharmacy_detail.html", page_data=data)
    else:
        pharmacy = Pharmacy.query.filter_by(pharmacy_id=current_user.pharmacy_id)
        updated_fields=pharmacy_schema.dump(request.form)
        errors = pharmacy_update_schema.validate(updated_fields)

    if errors:
        raise ValidationError(message=errors)
    else:
        pharmacy.update(updated_fields)
        db.session.commit()
        return redirect(url_for("pharmacies.get_pharmacies"))

@pharmacies.route('/pharmacies/<int:id>/edit/', methods=["PUT", "PATCH"])
def edit_pharmacy_member():
    return """This page will allow the pharmacy_member to add/remove vaccination certificate icon. Will also be able to edit information on a specific pharmacy - particularly their name, dob, isadmin status.
    Will also contain contact details and emergency contact details. All three sections will have different forms.
    Can only be access by admin or the particular pharmacy for pharmacies and/or pharmacy logged in. Should also be able to remove here"""

@pharmacies.route('/pharmacies/<int:id>/edit/', methods=["DELETE"])
def remove_pharmacy_member(id):
    return f'This will remove pharmacy member with specific {id}'

@pharmacies.route("/pharmacies/signup/", methods = ["GET", "POST"])
def pharmacies_signup():
    data = {
        "page_title": "Pharmacies SignUp Page"
    }
    if request.method == "GET":
        return render_template("signup.html", page_data=data)

    new_pharmacy = pharmacy_schema.load(request.form)
    db.session.add(new_pharmacy)
    db.session.commit()
    login_user(new_pharmacy)
    return redirect(url_for("pharmacies.get_pharmacies"))

@pharmacies.route('/pharmacies/login/', methods=["GET", "POST"])
def pharmacies_login():
    data = {
        "page_title":"Pharmacies LogIn page"
    }

    if request.method == "GET":
        return render_template("login.html", page_data=data)

    pharmacy = Pharmacy.query.filter_by(pharmacy_email=request.form["pharmacy_email"]).first()
    if pharmacy and pharmacy.check_password(password=request.form["pharmacy_password"]):
        login_user(pharmacy)
        return redirect(url_for('pharmacies.get_pharmacy_member'))
    
    abort(401, "Login Unsuccessful. Did you supply the correct username and password?")

@pharmacies.route("/pharmacies/logout/", methods = ["POST"])
@login_required
def pharmacies_logout():
    logout_user()
    return redirect(url_for("pharmacies.pharmacies_login"))