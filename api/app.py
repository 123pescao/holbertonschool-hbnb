#!/usr/bin/python3
from flask import Flask
from flask_restx import Api, Resource, fields
from datetime import datetime
import uuid

app = Flask(__name__)
api = Api(app, doc='/docs')

# Define the namespaces
place_ns = api.namespace('places', description='Places operations')
review_ns = api.namespace('reviews', description='Review operations')

# Place model definition
place_model = api.model('Place', {
    'id': fields.String(readonly=True, description='The place unique identifier'),
    'name': fields.String(required=True, description='The name of the place'),
    'description': fields.String(required=True, description='The description of the place'),
    'address': fields.String(required=True, description='The address of the place'),
    'city_id': fields.String(required=True, description='The ID of the city'),
    'latitude': fields.Float(required=True, description='The latitude of the place'),
    'longitude': fields.Float(required=True, description='The longitude of the place'),
    'host_id': fields.String(required=True, description='The ID of the host'),
    'number_of_rooms': fields.Integer(required=True, description='The number of rooms in the place'),
    'number_of_bathrooms': fields.Integer(required=True, description='The number of bathrooms in the place'),
    'price_per_night': fields.Float(required=True, description='The price per night'),
    'max_guests': fields.Integer(required=True, description='The maximum number of guests'),
    'amenity_ids': fields.List(fields.String, required=True, description='The list of amenity IDs')
})

# Review model definition
review_model = api.model('Review', {
    'id': fields.String(readonly=True, description='The review unique identifier'),
    'place_id': fields.String(required=True, description='The ID of the place being reviewed'),
    'user_id': fields.String(required=True, description='The ID of the user who wrote the review'),
    'rating': fields.Integer(required=True, description='Rating given by the user (1 to 5)'),
    'comment': fields.String(required=True, description='Review comment'),
    'created_at': fields.DateTime(readonly=True, description='Creation timestamp'),
    'updated_at': fields.DateTime(readonly=True, description='Last update timestamp')
})

# Mock data manager (to be replaced with actual data handling logic)
class DataManager:
    def __init__(self):
        self.storage = {"Place": {}, "Review": {}, "City": {}, "Amenity": {}, "User": {}}

    def get(self, id, entity):
        return self.storage.get(entity, {}).get(id)

    def save(self, entity):
        self.storage[type(entity).__name__].update({entity.id: entity})

    def update(self, entity):
        self.storage[type(entity).__name__][entity.id] = entity

    def delete(self, id, entity):
        if id in self.storage.get(entity, {}):
            del self.storage[entity][id]

    def get_all_reviews_by_place(self, place_id):
        return [review for review in self.storage.get("Review", {}).values() if review.place_id == place_id]

    def get_all_reviews_by_user(self, user_id):
        return [review for review in self.storage.get("Review", {}).values() if review.user_id == user_id]

data_manager = DataManager()

# Place endpoints
@place_ns.route('/')
class PlaceList(Resource):
    @place_ns.doc('list_places')
    @place_ns.marshal_list_with(place_model)
    def get(self):
        """List all places"""
        places = list(data_manager.storage["Place"].values())
        return places

    @place_ns.doc('create_place')
    @place_ns.expect(place_model)
    @place_ns.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = api.payload
        required_fields = ["name", "description", "address", "city_id", "latitude", "longitude", "host_id", "number_of_rooms", "number_of_bathrooms", "price_per_night", "max_guests", "amenity_ids"]
        if not all(field in data for field in required_fields):
            api.abort(400, "Missing required fields")

        if not isinstance(data["amenity_ids"], list):
            api.abort(400, "amenity_ids should be a list")

        if not (-90 <= data["latitude"] <= 90) or not (-180 <= data["longitude"] <= 180):
            api.abort(400, "Invalid geographical coordinates")

        if any(data[field] < 0 for field in ["number_of_rooms", "number_of_bathrooms", "max_guests"]):
            api.abort(400, "Room, bathroom, and guest capacities must be non-negative integers")

        if data["price_per_night"] < 0:
            api.abort(400, "Price per night must be a positive value")

        if data_manager.get(data["city_id"], "City") is None:
            api.abort(404, "City not found")

        for amenity_id in data["amenity_ids"]:
            if data_manager.get(amenity_id, "Amenity") is None:
                api.abort(404, f"Amenity {amenity_id} not found")

        place = {
            'id': str(uuid.uuid4()),
            'name': data["name"],
            'description': data["description"],
            'address': data["address"],
            'city_id': data["city_id"],
            'latitude': data["latitude"],
            'longitude': data["longitude"],
            'host_id': data["host_id"],
            'number_of_rooms': data["number_of_rooms"],
            'number_of_bathrooms': data["number_of_bathrooms"],
            'price_per_night': data["price_per_night"],
            'max_guests': data["max_guests"],
            'amenity_ids': data["amenity_ids"]
        }
        data_manager.save(place)
        return place, 201

@place_ns.route('/<string:place_id>')
@place_ns.doc(params={'place_id': 'The place unique identifier'})
class PlaceResource(Resource):
    @place_ns.doc('get_place')
    @place_ns.marshal_with(place_model)
    def get(self, place_id):
        """Get a place by ID"""
        place = data_manager.get(place_id, "Place")
        if place is None:
            api.abort(404, "Place not found")
        return place

    @place_ns.doc('update_place')
    @place_ns.expect(place_model)
    @place_ns.marshal_with(place_model)
    def put(self, place_id):
        """Update a place"""
        data = api.payload
        place = data_manager.get(place_id, "Place")
        if place is None:
            api.abort(404, "Place not found")

        if "latitude" in data and not (-90 <= data["latitude"] <= 90):
            api.abort(400, "Invalid latitude")
        if "longitude" in data and not (-180 <= data["longitude"] <= 180):
            api.abort(400, "Invalid longitude")
        if any(field in data and data[field] < 0 for field in ["number_of_rooms", "number_of_bathrooms", "max_guests"]):
            api.abort(400, "Room, bathroom, and guest capacities must be non-negative integers")
        if "price_per_night" in data and data["price_per_night"] < 0:
            api.abort(400, "Price per night must be a positive value")
        if "city_id" in data and data_manager.get(data["city_id"], "City") is None:
            api.abort(404, "City not found")
        if "amenity_ids" in data:
            if not isinstance(data["amenity_ids"], list):
                api.abort(400, "amenity_ids should be a list")
            for amenity_id in data["amenity_ids"]:
                if data_manager.get(amenity_id, "Amenity") is None:
                    api.abort(404, f"Amenity {amenity_id} not found")

        place.update({
            'name': data.get("name", place['name']),
            'description': data.get("description", place['description']),
            'address': data.get("address", place['address']),
            'city_id': data.get("city_id", place['city_id']),
            'latitude': data.get("latitude", place['latitude']),
            'longitude': data.get("longitude", place['longitude']),
            'host_id': data.get("host_id", place['host_id']),
            'number_of_rooms': data.get("number_of_rooms", place['number_of_rooms']),
            'number_of_bathrooms': data.get("number_of_bathrooms", place['number_of_bathrooms']),
            'price_per_night': data.get("price_per_night", place['price_per_night']),
            'max_guests': data.get("max_guests", place['max_guests']),
            'amenity_ids': data.get("amenity_ids", place['amenity_ids'])
        })
        data_manager.update(place)
        return place

    @place_ns.doc('delete_place')
    def delete(self, place_id):
        """Delete a place"""
        place = data_manager.get(place_id, "Place")
        if place is None:
            api.abort(404, "Place not found")
        data_manager.delete(place_id, "Place")
        return '', 204

# Review endpoints
@review_ns.route('/places/<string:place_id>/reviews')
class ReviewList(Resource):
    @review_ns.doc('list_reviews')
    @review_ns.marshal_list_with(review_model)
    def get(self, place_id):
        """List all reviews for a place"""
        reviews = data_manager.get_all_reviews_by_place(place_id)
        if not reviews:
            api.abort(404, "No reviews found for this place")
        return reviews

    @review_ns.doc('create_review')
    @review_ns.expect(review_model)
    @review_ns.marshal_with(review_model, code=201)
    def post(self, place_id):
        """Create a new review for a place"""
        data = api.payload
        required_fields = ["user_id", "rating", "comment"]
        if not all(field in data for field in required_fields):
            api.abort(400, "Missing required fields")

        if not 1 <= data["rating"] <= 5:
            api.abort(400, "Rating must be between 1 and 5")

        if data_manager.get(place_id, "Place") is None:
            api.abort(404, "Place not found")

        review = {
            'id': str(uuid.uuid4()),
            'place_id': place_id,
            'user_id': data["user_id"],
            'rating': data["rating"],
            'comment': data["comment"],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        data_manager.save(review)
        return review, 201

@review_ns.route('/users/<string:user_id>/reviews')
class UserReviewList(Resource):
    @review_ns.doc('list_user_reviews')
    @review_ns.marshal_list_with(review_model)
    def get(self, user_id):
        """List all reviews by a user"""
        reviews = data_manager.get_all_reviews_by_user(user_id)
        if not reviews:
            api.abort(404, "No reviews found for this user")
        return reviews

if __name__ == '__main__':
    app.run(debug=True)
