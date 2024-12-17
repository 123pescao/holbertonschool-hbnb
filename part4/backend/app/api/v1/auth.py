#!/usr/bin/python3
"""Defines authentication operations using Flask and JWT."""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Models for request payloads
register_model = api.model('Register', {
    'username': fields.String(required=True, description='User username'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Route: Register
@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        """Register a new user"""
        data = api.payload

        # Validate input fields
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return {'error': 'Missing required fields'}, 400

        # Check if user already exists
        if facade.get_user_by_email(data['email']):
            return {'error': 'User already exists'}, 409

        # Create and save the new user
        new_user = facade.create_user(
            data['username'],
            data['email'],
            data['password']
        )

        return {'message': 'User registered successfully', 'user_id': str(new_user.id)}, 201

# Route: Login
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        # Retrieve user and validate credentials
        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Generate JWT token
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        return {'access_token': access_token}, 200

# Route: Protected (Example for JWT Authentication)
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user["id"]}'}, 200
