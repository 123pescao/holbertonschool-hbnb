#!/usr/bin/python3
"""Users Endpoints"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade


api = Namespace('users', description='User operations')


user_model = api.model('User',{
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password for the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created')
    @api.response(400, 'Email exists')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already exists'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'message': 'User created',
            }
        except ValueError as e:
            return {'error': str(e)}, 400


    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get a list of all users"""
        users = facade.get_all_users()
        return [{
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
        }for user in users], 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        user_data = api.payload
        user = facade.get_user(user_id)

        if current_user.get('id') != user.id:
            return {'error': 'Unauthorized action'}, 403

        if not user:
            return {'error': 'User not found'}, 404

        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password.'}, 400

        allowed_updates = {
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name')
        }

        user.update(allowed_updates)
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }, 200