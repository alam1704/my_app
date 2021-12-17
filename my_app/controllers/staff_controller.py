from flask import Blueprint, request, render_template, redirect, url_for, abort, flash
from main import db, lm
from models.staffs import Staff
from schemas.staff_schema import staffs_schema, staff_schema, staff_update_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError

@lm.user_loader
def load_user(staff):
    return Staff.query.get(staff)

@lm.unauthorized_handler
def unauthorized():
    return redirect("/login/")

staffs = Blueprint('staffs', __name__)
# Now register this new controller by adding it into the __init__.py file

@staffs.route('/staffs/', methods=["GET"])
def get_staffs():
    data = {
        "page_title": "Staffs Index",
        "staffs": staffs_schema.dump(Staff.query.all())
    }
    return render_template("staffs_index.html", page_data=data)

@staffs.route('/staffs/account/', methods=["GET", "POST"])
@login_required
def get_staff_member():
    if request.method == "GET":
        data = {
            "page_title":"Your Account details"
        }
        return render_template("staff_detail.html", page_data=data)
    else:
        staff = Staff.query.filter_by(staff_id=current_user.staff_id)
        updated_fields=staff_schema.dump(request.form)
        errors = staff_update_schema.validate(updated_fields)

    if errors:
        raise ValidationError(message=errors)
    else:
        staff.update(updated_fields)
        db.session.commit()
        return redirect(url_for("staffs.get_staffs"))

@staffs.route('/staffs/<int:id>/edit/', methods=["PUT", "PATCH"])
def edit_staff_member():
    return """This page will allow the staff_member to add/remove vaccination certificate icon. Will also be able to edit information on a specific staff - particularly their name, dob, isadmin status.
    Will also contain contact details and emergency contact details. All three sections will have different forms.
    Can only be access by admin or the particular staff for pharmacies and/or staff logged in. Should also be able to remove here"""

@staffs.route('/staffs/<int:id>/edit/', methods=["DELETE"])
def remove_staff_member(id):
    return f'This will remove staff member with specific {id}'

@staffs.route("/staffs/signup/", methods = ["GET", "POST"])
def staffs_signup():
    data = {
        "page_title": "Staffs SignUp"
    }
    if request.method == "GET":
        return render_template("signup.html", page_data=data)

    new_staff = staff_schema.load(request.form)
    db.session.add(new_staff)
    db.session.commit()
    login_user(new_staff)
    return redirect(url_for("staffs.get_staffs"))

@staffs.route('/staffs/login/', methods=["GET", "POST"])
def staffs_login():
    data = {
        "page_title":"Staffs LogIn"
    }

    if request.method == "GET":
        return render_template("login.html", page_data=data)

    staff = Staff.query.filter_by(staff_name=request.form["staff_name"]).first()
    if staff and staff.check_password(password=request.form["staff_password"]):
        login_user(staff)
        return redirect(url_for('staffs.get_staff_member'))
    
    abort(401, "Login Unsuccessful. Did you supply the correct username and password?")

@staffs.route("/staffs/logout/", methods = ["POST"])
@login_required
def staffs_logout():
    logout_user()
    return redirect(url_for("staffs.staffs_login"))