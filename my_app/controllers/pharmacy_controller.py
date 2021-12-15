from flask import Blueprint, jsonify, request
from main import db
from models.pharmacies import Pharmacy

pharmacies = Blueprint('pharmacies', __name__)

@pharmacies.route('/home/')
def home_page():
    return "This page will ask the user if they are a pharmacy(admin) or a staff. After selecting which one they are, they'll be directed to either log in pages"

@pharmacies.route('/pharmacy_login/')
def pharmacy_login():
    return "This page will display the pharmacy log in page"

@pharmacies.route('/staff_login/')
def staff_login():
    return "This page will display the staff log in page"

@pharmacies.route('/pharmacies/', methods=["GET"])
def pharmacies():
    pharmacies = Pharmacy.query.all()
    return jsonify([pharmacy.serialize for pharmacy in pharmacies])

@pharmacies.route('/pharmacies/', methods=["POST"])
def create_pharmacy():
    new_pharmacy = Pharmacy(request.json['pharmacy_name'])
    db.session.add(new_pharmacy)
    db.session.commit()
    return jsonify(new_pharmacy.serialize)

@pharmacies.route('/pharmacies/<int:pharmacy_id>/', methods=["GET"])
def pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    return jsonify(pharmacy.serialize)

@pharmacies.route('/pharmacies/<int:pharmacy_id>/edit/', methods=["PUT","PATCH"])
def edit_pharmacy(id):
    pharmacy = Pharmacy.query.filter_by(pharmacy_id=id)
    pharmacy.update(dict(pharmacy_name = request.json["pharmacy_name"]))
    db.session.commit()
    return jsonify(pharmacy.first().serialize)

@pharmacies.route('/pharmacies/<int:pharmacy_id>/edit/', methods=["DELETE"])
def remove_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    db.session.delete(pharmacy)
    db.session.commit()
    return jsonify(pharmacy.serialize)

@pharmacies.route('/staff/', methods=["GET"])
def staff():
    return "This page will display a list of all staff for pharmacies logged in"

@pharmacies.route('/staff/<int:staff_id>/', methods=["GET"])
def staff_member():
    return """This page will show the specific staff_member's vaccination certificate. Will also return information on a specific staff - particularly their name, dob, isadmin status.
    Will also contain contact details and emergency contact details. All three sections will have different forms.
    Can only be access by admin or the particular staff for pharmacies and/or staff logged in"""

@pharmacies.route('/staff/<int:staff_id>/edit/')
def edit_staff_member():
    return """This page will allow the staff_member to add/remove vaccination certificate icon. Will also be able to edit information on a specific staff - particularly their name, dob, isadmin status.
    Will also contain contact details and emergency contact details. All three sections will have different forms.
    Can only be access by admin or the particular staff for pharmacies and/or staff logged in. Should also be able to remove here"""