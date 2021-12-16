from flask.json import dump
from sqlalchemy.orm import load_only
from main import ma
from models.staffs import Staff
from marshmallow_sqlalchemy import auto_field
from marshmallow import fields, exceptions, validate
from werkzeug.security import generate_password_hash

class StaffSchema(ma.SQLAlchemyAutoSchema):
    staff_id = auto_field(dump_only=True)
    staff_name = auto_field(required=True, validate=validate.Length(min=1))
    staff_dob = auto_field(required=True)
    staff_password = fields.Method(
        required=True,
        load_only=True,
        deserialize="load_password"
    )

    def load_password(self, password):
        if len(password)>6:
            return generate_password_hash(password, method="sha256")
        raise exceptions.ValidationError("Password must be at least characters.")
    
    class Meta:
        model = Staff
        load_instance = True

staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)
staff_update_schema = StaffSchema(partial=True)