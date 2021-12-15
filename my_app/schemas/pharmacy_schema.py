from main import ma
from models.pharmacies import Pharmacy
from marshmallow_sqlalchemy import auto_field

class PharmacySchema(ma.SQLAlchemyAutoSchema):
    pharmacy_id = auto_field(dump_only=True)

    class Meta:
        model = Pharmacy
        load_instance = True
    
pharmacy_schema = PharmacySchema()
pharmacies_schema = PharmacySchema(many=True)