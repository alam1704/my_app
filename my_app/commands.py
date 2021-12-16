from main import db
from flask import Blueprint
from random import randint

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    "Creating all of the tables. Need to make sure that we run sudo service postgresql start before running command."
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_db():
    "Deleting all of the tables"
    db.drop_all()
    print("Tables deleted")

@db_commands.cli.command("seed")
def seed_db():
    from models.pharmacies import Pharmacy
    from faker import Faker
    faker = Faker()

    for i in range(20):
        pharmacy = Pharmacy(faker.catch_phrase(), faker.company_email(), randint(0, 1))
        db.session.add(pharmacy)
    
    db.session.commit()
    print("Tables seeded")
