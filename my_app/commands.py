from main import db
from flask import Blueprint
from random import randint

db_commands = Blueprint("db-custom", __name__)

@db_commands.cli.command("create")
def create_db():
    "Creating all of the tables. Need to make sure that we run sudo service postgresql start before running command."
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    "Deleting all of the tables"
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():
    from models.pharmacies import Pharmacy
    from models.staffs import Staff
    from faker import Faker
    fake = Faker()

    for i in range(5):
        pharmacy = Pharmacy(
            pharmacy_name = fake.name(), 
            pharmacy_email = fake.email(),
            pharmacy_phone = fake.msisdn()[3:10],
            pharmacy_password = fake.text()[6:10]
        )
        db.session.add(pharmacy)
    
    db.session.commit()

    # get pharmacy from database
    pharmacies = Pharmacy.query.all()

    for pharmacy in pharmacies:
        # get 5 staff members
        for i in range(5):
            staff = Staff(
                staff_name = fake.name(),
                staff_email = fake.email(),
                staff_dob = fake.date_of_birth(),
                staff_salary= fake.random_int(min=0, max=999999)
            )
            db.session.add(staff)
    db.session.commit()
    
    print("Tables seeded")

@db_commands.cli.command("reset")
def reset_db():
    """Drops, create, and seeds tables in one step"""
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted!")
    db.create_all()
    print("Tables created!")
    from models.pharmacies import Pharmacy
    from faker import Faker
    faker = Faker()

    for i in range(20):
        pharmacy = Pharmacy(faker.catch_phrase(), faker.company_email(), randint(0, 1))
        db.session.add(pharmacy)
    
    db.session.commit()
    print("Tables seeded")


