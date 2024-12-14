#!/usr/bin/python3
"""Initialize Flask App"""
from flask import Flask
from flask_restx import Api
from config import config
from app.extensions import db, bcrypt, jwt
from .api.v1.users import api as users_ns
from .api.v1.places import api as places_ns
from .api.v1.reviews import api as reviews_ns
from .api.v1.amenities import api as amenities_ns
from .api.v1.auth import api as auth_ns
from .api.v1.admin import api as admin_ns


def create_app(config_class="config.DevelopmentConfig"):
        app = Flask(__name__)
        app.config.from_object(config_class)

        # Initialize the extensions
        db.init_app(app)
        bcrypt.init_app(app)
        jwt.init_app(app)

        authorizations = {
                "BearerAuth": {
                        "type": "apiKey",
                        "name": "Authorization",
                        "in": "header",
                }
        }

        # Set up the API
        api = Api(
                app,
                version='1.0',
                title='HBnB API',
                description='HBnB Application API',
                authorizations=authorizations,
                security="BearerAuth",
        )
        #Register namespace
        api.add_namespace(users_ns, path='/api/v1/users')
        api.add_namespace(places_ns, path='/api/v1/places')
        api.add_namespace(reviews_ns, path='/api/v1/reviews')
        api.add_namespace(amenities_ns, path='/api/v1/amenities')
        api.add_namespace(auth_ns, path='/api/v1/auth')
        api.add_namespace(admin_ns, path='/api/v1/admin')

        return app

