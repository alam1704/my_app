from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Staff(UserMixin, db.Model):
    __tablename__ = "staff"

    staff_id = db.Column(
        db.Integer,
        primary_key=True
    )

    staff_name = db.Column(
        db.String(100),
        nullable=False
    )

    staff_dob = db.Column(
        db.Integer,
        nullable=False
    )

    staff_password = db.Column(
        db.String(200),
        nullable=False
    )
    staff_is_admin = db.Column(
        db.Boolean(),
        nullable=False,
        server_default="False"
    )

    def get_id(self):
        return self.staff_id
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    contactdetails = db.relationship("ContactDetails", back_populates="staff", uselist=False)

class ContactDetails(db.Model):
    __tablename__ = "contactdetails"

    contactdetails_id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Add other attributes here

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("staff.staff_id")
    )

    staff = db.relationship("Staff", back_populates="contactdetails")
    econtactdetails = db.relationship("EContactDetails", back_populates="contactdetails", uselist=False)

class EContactDetails(db.Model):
    __tablename__ = "econtactdetails"

    econtactdetails_id = db.Column(
        db.Integer,
        primary_key=True
    )

    # add other attributes here

    contactdetails_id = db.Column(
        db.Integer,
        db.ForeignKey("contactdetails.contactdetails_id")
    )

    contactdetails = db.relationship("ContactDetails", back_populates="econtactdetails")