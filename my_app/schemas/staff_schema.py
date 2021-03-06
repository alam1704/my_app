from main import ma
from models.staffs import Staff
from marshmallow_sqlalchemy import auto_field
from marshmallow.validate import Length, Email, Range

class StaffSchema(ma.SQLAlchemyAutoSchema):
    staff_id = auto_field(dump_only=True)
    staff_name = auto_field(required=True, validate=Length(min=1, max=50))
    staff_email = auto_field(required=True, validate = Email())
    staff_dob = auto_field(required=False, validate=Length(min=1))
    staff_salary = auto_field(required=False, validate=Range(0, 999999))
    creator = ma.Nested("PharmacySchema")

    class Meta:
        model = Staff
        load_instance = True
    
staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)