#!/usr/bin/python3
"""Places endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Review update model
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=True, description='Updated review text'),
    'rating': fields.Integer(required=True, description='Updated rating (1-5)')
})

# Place model
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities IDs")
})

# ----------------------- PLACE ROUTES -----------------------
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload

        try:
            # Ensure current user matches owner_id
            if place_data['owner_id'] != current_user['id']:
                return {'error': 'Unauthorized action'}, 403

            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id,
                'amenities': [a.id for a in new_place.amenities]
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [{
            'id': place.id,
            'title': place.title,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places], 200

# ----------------------- PLACE BY ID -----------------------
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get details of a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities],
            'reviews': [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in place.reviews]
        }, 200

# ----------------------- PLACE REVIEWS -----------------------
@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [
            {'id': r.id, 'text': r.text, 'rating': r.rating, 'user_id': r.user_id}
            for r in reviews
        ], 200

    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, place_id):
        """Update an existing review for a specific place"""
        current_user = get_jwt_identity()
        review_data = api.payload

        # Find the review
        review = facade.get_review_by_place_and_user(place_id, current_user['id'])
        if not review:
            return {'error': 'Review not found or unauthorized'}, 404

        try:
            updated_review = facade.update_review(review.id, review_data)
            return {
                'message': 'Review updated successfully',
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
