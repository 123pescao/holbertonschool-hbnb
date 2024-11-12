"""Initialize Flask App"""
from flask import Flask
from flask_restx import Api
from .extensions import db, bcrypt, migrate
from .api.v1.users import api as users_ns
from .api.v1.places import api as places_ns
from .api.v1.reviews import api as reviews_ns
from .api.v1.amenities import api as amenities_ns

def create_app(config_class="config.DevelopmentConfig"):
        app = Flask(__name__)
        app.config.from_object(config_class)
        migrate.init_app(app, db)

        # Initialize the extensions
        db.init_app(app)
        bcrypt.init_app(app)
        migrate.init_app(app, db)

        # Set up the API
        api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
        api.add_namespace(users_ns, path='/api/v1/users')
        api.add_namespace(places_ns, path='/api/v1/places')
        api.add_namespace(reviews_ns, path='/api/v1/reviews')
        api.add_namespace(amenities_ns, path='/api/v1/amenities')

        # Import models here so they are registered with the SQLAlchemy instance
        with app.app_context():
                from app.models.user import User
                from app.models.place import Place
                from app.models.review import Review
                from app.models.amenity import Amenity

        return app

