from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Pharmacy(UserMixin, db.Model):
    __tablename__ = "pharmacy"

    pharmacy_id = db.Column(
        db.Integer,
        primary_key=True
    )

    pharmacy_name = db.Column(
        db.String(100),
        nullable=False
    )
    
    pharmacy_email = db.Column(
        db.String(100),
        nullable=False
    )

    pharmacy_phone = db.Column(
        db.String(20),
        nullable=False
    )
    
    pharmacy_password = db.Column(
        db.String(200),
        nullable=False
    )
    pharmacy_is_admin = db.Column(
        db.Boolean(),
        nullable=False,
        server_default="False"
    )

    staffs = db.relationship(
        'Staff',
        backref="creator"
    )

    def get_id(self):
        return self.pharmacy_id
 
    def check_password(self, password):
        return check_password_hash(self.pharmacy_password, password)







