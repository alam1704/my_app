from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

(
    db_user, 
    db_pass, 
    db_name, 
    db_domain
) = (os.environ.get(item) for item in [
    "DB_USER", 
    "DB_PASS", 
    "DB_NAME", 
    "DB_DOMAIN"
    ]
)

# Creating the Flask app object
app = Flask(__name__)

# Configuring our app:
# Tells the app where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_domain}/{db_name}"
# This setting prevents Flask from shouting warnings at us
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Creating the database object - allowing us to use the ORM
db = SQLAlchemy(app)

# Pharmacy table in the database
class Pharmacy(db.Model):
    # specifies what the name of table should be 
    __tablename__ = "pharmacies"

    # specifies what the columns of the table should be
    pharmacy_id = db.Column(db.Integer, primary_key=True)
    pharmacy_name = db.Column(db.String(100), unique=True, nullable=False)
    pharmacy_email = db.Column(db.String(100), unique=True, nullable=False)
    pharmacy_phone = db.Column(db.Integer, unique=True, nullable=False)

    # Creates a python object to insert as a new row
    def __init__(self,pharmacy_name):
        self.pharmacy_name=pharmacy_name

    # Serialize property lets us convert our Pharmacy object into JSON easily.
    @property
    def serialize(self):
        return {
            "pharmacy_id": self.pharmacy_id,
            "pharmacy_name": self.pharmacy_name,
            "pharmacy_email": self.pharmacy_email,
            "pharmacy_phone": self.pharmacy_phone
        }

# Create any database tables that don't already exist
db.create_all()


@app.route('/home/')
def home_page():
    return "This page will ask the user if they are a pharmacy(admin) or a staff. After selecting which one they are, they'll be directed to either log in pages"

@app.route('/pharmacy_login/')
def pharmacy_login():
    return "This page will display the pharmacy log in page"

@app.route('/staff_login/')
def staff_login():
    return "This page will display the staff log in page"

@app.route('/pharmacies/', methods=["GET"])
def pharmacies():
    pharmacies = Pharmacy.query.all()
    return jsonify([pharmacy.serialize for pharmacy in pharmacies])

@app.route('/pharmacies/', methods=["POST"])
def create_pharmacy():
    new_pharmacy = Pharmacy(request.json['pharmacy_name'])
    db.session.add(new_pharmacy)
    db.session.commit()
    return jsonify(new_pharmacy.serialize)

@app.route('/pharmacies/<int:pharmacy_id>/', methods=["GET"])
def pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    return jsonify(pharmacy.serialize)

@app.route('/pharmacies/<int:pharmacy_id>/edit/', methods=["PUT","PATCH"])
def edit_pharmacy(id):
    pharmacy = Pharmacy.query.filter_by(pharmacy_id=id)
    pharmacy.update(dict(pharmacy_name = request.json["pharmacy_name"]))
    db.session.commit()
    return jsonify(pharmacy.first().serialize)

@app.route('/pharmacies/<int:pharmacy_id>/edit/', methods=["DELETE"])
def remove_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    db.session.delete(pharmacy)
    db.session.commit()
    return jsonify(pharmacy.serialize)

@app.route('/staff/', methods=["GET"])
def staff():
    return "This page will display a list of all staff for pharmacies logged in"

@app.route('/staff/<int:staff_id>/', methods=["GET"])
def staff_member():
    return """This page will show the specific staff_member's vaccination certificate. Will also return information on a specific staff - particularly their name, dob, isadmin status.
    Will also contain contact details and emergency contact details. All three sections will have different forms.
    Can only be access by admin or the particular staff for pharmacies and/or staff logged in"""

@app.route('/staff/<int:staff_id>/edit/')
def edit_staff_member():
    return """This page will allow the staff_member to add/remove vaccination certificate icon. Will also be able to edit information on a specific staff - particularly their name, dob, isadmin status.
    Will also contain contact details and emergency contact details. All three sections will have different forms.
    Can only be access by admin or the particular staff for pharmacies and/or staff logged in. Should also be able to remove here"""




if __name__ == '__main__':
    app.run(debug=True)