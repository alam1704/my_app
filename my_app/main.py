from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():

    # Creating the Flask app object
    app = Flask(__name__)

    # Configuring our app:
    app.config.from_object("config.app_config")

    # Creating a generic object that can import our models code
    db.init_app(app)

    # To register our routes
    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app