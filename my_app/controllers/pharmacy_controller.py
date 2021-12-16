from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from werkzeug.utils import redirect
from main import db
from models.pharmacies import Pharmacy
from schemas.pharmacy_schema import pharmacies_schema, pharmacy_schema

pharmacies = Blueprint('pharmacies', __name__)

@pharmacies.route('/home/', methods=["GET"])
def home_page():
    data = {
        "page_title": "Home"
    }
    return render_template("home.html", page_data=data)

@pharmacies.route('/pharmacy_login/')
def pharmacy_login():
    return "This page will display the pharmacy log in page" 

@pharmacies.route('/pharmacies/', methods=["GET"])
def get_pharmacies():
    pharmacies = Pharmacy.query.all()
    data = {
        "page_title": "Pharmacies Index",
        "pharmacies":pharmacies_schema.dump(pharmacies)
    }
    
    return render_template("pharmacies_index.html", page_data=data)

@pharmacies.route('/pharmacies/', methods=["POST"])
def create_pharmacy():
    new_pharmacy = pharmacy_schema.load(request.form)
    db.session.add(new_pharmacy)
    db.session.commit()
    return redirect(url_for("pharmacies.get_pharmacies"))

@pharmacies.route('/pharmacies/<int:id>/', methods=["GET"])
def get_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    data = {
        "page_title" : "Pharmacy Detail",
        "pharmacy" : pharmacy_schema.dump(pharmacy)
    }
    return render_template("pharmacy_detail.html", page_data=data)

@pharmacies.route('/pharmacies/<int:id>/', methods=["POST"])
def edit_pharmacy(id):
    pharmacy = Pharmacy.query.filter_by(pharmacy_id=id)
    updated_fields = pharmacy_schema.dump(request.form)
    print(updated_fields)
    if updated_fields:
        pharmacy.update(updated_fields)
        db.session.commit()
    data = {
        "page_title": "Pharmacy Details",
        "pharmacy": pharmacy_schema.dump(pharmacy.first()) 
    }
    
    return render_template("pharmacy_detail.html", page_data=data)

@pharmacies.route('/pharmacies/<int:id>/delete/', methods=["POST"])
def remove_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    db.session.delete(pharmacy)
    db.session.commit()
    return redirect(url_for("pharmacies.get_pharmacies"))


