from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.exceptions import ValidationError
from flask_login import LoginManager
import os

db = SQLAlchemy()
ma = Marshmallow()
lm = LoginManager()

def create_app():

    # Creating the Flask app object
    app = Flask(__name__)

    # Configuring our app:
    app.config.from_object("config.app_config")

    # Creating a generic object that can import our models code
    db.init_app(app)
    ma.init_app(app)
    lm.init_app(app)

    # register the CLI commands blueprint on the app
    from commands import db_commands
    app.register_blueprint(db_commands)

    # To register our routes
    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    @app.errorhandler(ValidationError)
    def handle_bad_request(error):
        return(jsonify(error.messages), 400)

    return app