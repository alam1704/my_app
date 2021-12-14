from flask import Flask 

app = Flask(__name__)

@app.route('/home/')
def home_page():
    return "This page will ask the user if they are a pharmacy(admin) or a staff. After selecting which one they are, they'll be directed to either log in pages"

@app.route('/pharmacy_login/')
def pharmacy_login():
    return "This page will display the pharmacy log in page"

@app.route('/staff_login/')
def staff_login():
    return "This page will display the staff log in page"

@app.route('/pharmacies/')
def pharmacies():
    return "This page will display a list of all pharmacies for pharmacies logged in"

@app.route('/pharmacies/<int:pharmacy_id>/')
def pharmacy():
    return "This page will display details of the pharmacy including name, email, phone and address for pharmacies logged in"

@app.route('/pharmacies/<int:pharmacy_id>/edit/')
def edit_pharmacy():
    return "This page will allow details of the pharmacy including name, email, phone and address to be edited by pharmacies logged in. Should also be able to remove here."

@app.route('/staff/')
def staff():
    return "This page will display a list of all staff for pharmacies logged in"

@app.route('/staff/<int:staff_id>/')
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