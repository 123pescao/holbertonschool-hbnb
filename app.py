#!/usr/bin/python3
from flask import Flask, request, jsonify
from models.data_manager import DataManager
from models.user import User
from models.review import Review
from models.country import Country
from models.city import City
from models.place import Place
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='HBnB Evolution API', description='A simple HBnB Evolution API')
data_manager = DataManager()

user_model = api.model('User', {
    'id': fields.String(readonly=True, description='The user unique identifier'),
    'email': fields.String(required=True, description='The user email'),
    'first_name': fields.String(required=True, description='The user first name'),
    'last_name': fields.String(required=True, description='The user last name'),
    'created_at': fields.String(readonly=True, description='The user creation date'),
    'updated_at': fields.String(readonly=True, description='The user last update date')})

@api.route('/users')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        users = data_manager.get_all('User')
        return users, 200

    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = api.payload
        if not data or 'email' not in data or 'first_name' not in data or 'last_name' not in data:
            api.abort(400, "Missing required fields")

        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']

        if not validate_email(email):
            api.abort(400, "Invalid email format")
        if user_exists(email):
            api.abort(409, "Email already exists")

        user = User(email=email, first_name=first_name, last_name=last_name)
        data_manager.save(user)
        return user.to_dict(), 201

@api.route('/users/<string:user_id>')
class User(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = data_manager.get(user_id, 'User')
        if not user:
            api.abort(404, "User not found")
        return user, 200

    @api.doc('update_user')
    @api.expect(user_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        data = api.payload
        if not data or 'email' not in data or 'first_name' not in data or 'last_name' not in data:
            api.abort(400, "Missing required fields")

        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']

        if not validate_email(email):
            api.abort(400, "Invalid email format")

        user = data_manager.get(user_id, 'User')
        if not user:
            api.abort(404, "User not found")

        user['email'] = email
        user['first_name'] = first_name
        user['last_name'] = last_name
        data_manager.update(User(**user))
        return user, 200

    @api.doc('delete_user')
    def delete(self, user_id):
        user = data_manager.get(user_id, 'User')
        if not user:
            api.abort(404, "User not found")

        data_manager.delete(user_id, 'User')
        return '', 204

def validate_email(email):
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def user_exists(email):
    users = data_manager.get_all('User')
    for user in users:
        if user['email'] == email:
            return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
