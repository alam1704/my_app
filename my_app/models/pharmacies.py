from main import db
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

