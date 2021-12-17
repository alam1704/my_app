from enum import auto
from flask.json import dump
from sqlalchemy.orm import load_only
from main import ma
from models.pharmacies import Pharmacy
from marshmallow_sqlalchemy import auto_field
from marshmallow import fields, exceptions, validate
from werkzeug.security import generate_password_hash

class PharmacySchema(ma.SQLAlchemyAutoSchema):
    pharmacy_id = auto_field(dump_only=True)
    pharmacy_name = auto_field(required=True, validate=validate.Length(min=1))
    pharmacy_email = auto_field(required=True, validate = validate.Email())
    pharmacy_phone = auto_field(required=False, validate=validate.Length(min=1))
    pharmacy_password = fields.Method(
        required=True,
        load_only=True,
        deserialize="load_password"
    )

    def load_password(self, password):
        if len(password)>6:
            return generate_password_hash(password, method="sha256")
        raise exceptions.ValidationError("Password must be at least characters.")
    
    class Meta:
        model = Pharmacy
        load_instance = True

pharmacy_schema = PharmacySchema()
pharmacies_schema = PharmacySchema(many=True)
pharmacy_update_schema = PharmacySchema(partial=True)