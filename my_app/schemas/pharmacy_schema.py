from main import ma
from models.pharmacies import Pharmacy
from marshmallow import validate
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length

class PharmacySchema(ma.SQLAlchemyAutoSchema):
    pharmacy_id = auto_field(dump_only=True)
    pharmacy_name = auto_field(required=True, validate=Length(min=1))
    pharmacy_email = auto_field(required=True, validate = validate.Email())
    pharmacy_phone = auto_field(required=False)

    class Meta:
        model = Pharmacy
        load_instance = True
    
pharmacy_schema = PharmacySchema()
pharmacies_schema = PharmacySchema(many=True)