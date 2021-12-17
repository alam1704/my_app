from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app
from werkzeug.utils import redirect
from main import db
from models.staffs import Staff
from schemas.staff_schema import staffs_schema, staff_schema
from flask_login import login_required, current_user

staffs = Blueprint('staffs', __name__)

@staffs.route('/home/', methods=["GET"])
def home_page():
    data = {
        "page_title": "Home"
    }
    return render_template("home.html", page_data=data)

@staffs.route('/staff_login/')
def staff_login():
    return "This page will display the staff log in page" 

@staffs.route('/staffs/', methods=["GET"])
def get_staffs():
    staffs = Staff.query.all()
    data = {
        "page_title": "Staffs Index",
        "staffs":staffs_schema.dump(staffs)
    }
    
    return render_template("staffs_index.html", page_data=data)

@staffs.route('/staffs/', methods=["POST"])
@login_required
def create_staff():
    new_staff = staff_schema.load(request.form)
    new_staff.creator = current_user
    db.session.add(new_staff)
    db.session.commit()
    return redirect(url_for("staffs.get_staffs"))

@staffs.route('/staffs/<int:staff_id>/', methods=["GET"])
@login_required
def get_staff(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    data = {
        "page_title" : "Staff Detail",
        "staff" : staff_schema.dump(staff)
    }
    return render_template("staff_detail.html", page_data=data)

@staffs.route('/staffs/<int:staff_id>/', methods=["POST"])
def edit_staff(staff_id):
    staff = Staff.query.filter_by(staff_id=staff_id)
    updated_fields = staff_schema.dump(request.form)
    print(updated_fields)
    if updated_fields:
        staff.update(updated_fields)
        db.session.commit()
    data = {
        "page_title": "Staff Details",
        "staff": staff_schema.dump(staff.first()) 
    }
    
    return render_template("staff_detail.html", page_data=data)

@staffs.route('/staffs/<int:id>/delete/', methods=["POST"])
def remove_staff(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    db.session.delete(staff)
    db.session.commit()
    return redirect(url_for("staffs.get_staffs"))


