#!/usr/bin/python3
"""Users Endpoints"""
from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from app import bcrypt

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
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new user"""
        user_data = api.payload
        try:
            hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            user_data['password'] = hashed_password
            new_user = facade.create_user({
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'password': user_data['password'],
                'is_admin': bool(user_data.get('is_admin', False))
            })
            return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            } for user in users
        ], 200

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
    def put(self, user_id):
        """Update user details by ID"""
        user_data = api.payload
        if 'password' in user_data:
            user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200
