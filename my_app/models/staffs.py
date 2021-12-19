from main import db
# Pharmacy table in the database
class Staff(db.Model):
    # specifies what the name of table should be 
    __tablename__ = "staff"

    # specifies what the columns of the table should be
    staff_id = db.Column(db.Integer, primary_key=True)
    staff_name = db.Column(db.String(100), unique=True, nullable=False)
    staff_email = db.Column(db.String(100), unique=True, nullable=False)
    staff_dob = db.Column(db.String(100), nullable=False)
    staff_salary = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("pharmacy.pharmacy_id")
    )

    contactdetails = db.relationship("ContactDetails", back_populates="staff", uselist=False)
    certificates = db.relationship("Certificates", backref="staff", lazy=True)

    @property
    def image_filename(self):
        return f"{self.staff_id}_{self.staff_name}.pdf"

class ContactDetails(db.Model):
    __tablename__ = "contactdetails"

    contactdetails_id = db.Column(
        db.Integer,
        primary_key=True
    )

    contactdetails_phone = db.Column(
        db.String(20),
        nullable=True
    )

    contactdetails_unitno = db.Column(
        db.Integer,
        nullable=True
    )

    contactdetails_stadd = db.Column(
        db.String(200),
        nullable=True
    )

    contactdetails_postcode = db.Column(
        db.Integer,
        nullable=True
    )

    contactdetails_city = db.Column(
        db.String(100),
        nullable=True
    )

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("staff.staff_id"),
        unique=True
    )

    staff = db.relationship("Staff", back_populates="contactdetails")
    econtactdetails = db.relationship("EContactDetails", back_populates="contactdetails", uselist=False)

class EContactDetails(db.Model):
    __tablename__ = "econtactdetails"

    econtactdetails_id = db.Column(
        db.Integer,
        primary_key=True
    )

    econtactdetails_name= db.Column(
        db.String(100),
        nullable=True
    )

    econtactdetails_phone = db.Column(
        db.String(20),
        nullable=True
    )

    contactdetails_id = db.Column(
        db.Integer,
        db.ForeignKey("contactdetails.contactdetails_id"),
        unique=True
    )

    contactdetails = db.relationship("ContactDetails", back_populates="econtactdetails")

class Certificates(db.Model):
    __tablename__ = "certificates"

    certificate_id = db.Column(
        db.Integer,
        primary_key=True
    )

    certificate_url = db.Column(
        db.String(200),
        nullable=True
    )

    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("staff.staff_id"),
        unique=True
    )
