from flask_restx import Namespace, Resource
from namespaces.ns_naruc import api
from database import create_connection
from flask import request, jsonify
from bson.objectid import ObjectId
import bcrypt
import uuid
from models import login_model, user_model, user_password, user_model_signin
import datetime
import jwt
import os
from auth_middleware import token_required

# DB Connect
client, conn = create_connection()
db = client['naruc_app']

users_collection = db['users']


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }

        return jwt.encode(
            payload,
            os.environ.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e

#login 
class login(Resource):
    @api.doc(description="Login with email and password")
    @api.expect(login_model)
    def post(self):
        data = api.payload
        email = data['email']
        password = data['password']

        try:
            users_collection = db.users

            user = users_collection.find_one({'email': email})

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                user_data = {
                    '_id': user['_id'],
                    'name': user['name'],
                    'surname': user['surname'],
                    'email': user['email'],
                    'role': user['role'],
                    'token': encode_auth_token(user['_id'])
                }
                return user_data, 200
            else:
                return 'Not Found', 404
        except Exception as e:
            return str(e), 500

#add user
# @token_required
class sign_in(Resource):
    @api.doc(description="Create a new user", security="apikey")
    @token_required
    @api.expect(user_model_signin)
    def post(self):
        user_id = uuid.uuid4().hex
        api.payload['_id'] = user_id
        data = api.payload 
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            '_id': user_id, 
            'name': data['name'],
            'surname': data['surname'],
            'email': data['email'],
            'role': data['role'],
            'password': hashed_password
        }
        try:
            users_collection = db.users
            users_collection.insert_one(user_data)
            return 'User created', 200
        except Exception as e:
            return str(e), 500 

#get_users 
class get_users(Resource):
    @token_required
    @api.doc(description="Get information about all registered users", security='apikey')
    def get(self):
        try:
            users = list(db.users.find({}, {'password': 0}))
            
            if users:
                return users, 200
            else:
                return [], 200 
        except Exception as e:
            return str(e), 500 

#update_user_info 
class update_user_info(Resource):
     @api.expect(user_model)
     @token_required
     @api.doc(security="apikey")
     def put(self, user_id):
        data = request.json
        try:
            result = db.users.update_one({'_id': user_id}, {
                '$set': {
                    'name': data['name'],
                    'surname': data['surname'],
                    'email': data['email'],
                    'role': data['role'],
                }
            })
            if result.modified_count == 1:
                return 'User information updated successfully', 200
            else:
                return 'User not found', 404
        except Exception as e:
            return str(e), 500 

#update password
class update_user_password(Resource):
    @api.expect(user_password)
    @token_required
    @api.doc(security="apikey")
    def put(self, user_id):
        data = request.json
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        try:
            result = db.users.update_one({'_id': user_id}, {'$set': {'password': hashed_password}})
            if result.modified_count == 1:
                return {'message': 'User password changed successfully'}, 200
            else:
                return {'message': 'User not found'}, 404
        except Exception as e:
            return {'message': 'Server error'}, str(e),500

# Get user info
class get_user_info(Resource):
    @api.doc(description="Get information about a specific client by ID", security="apikey")
    @token_required
    def get(self, user_id):
        try:
            users = db.users.find_one({'_id': user_id}, {'password': 0})

            if users:
                return users, 200
            else:
                return {'message': 'Client not found'}, 404
        except Exception as e:
            return str(e), 500

#delete user by id 
class delete_user(Resource):
    @token_required
    @api.doc(security="apikey")
    def delete(self, user_id):
        try:
            result = db.users.delete_one({'_id':user_id})
            if result.deleted_count == 1:
                return 'User was deleted', 202
            else:
                return 'User not found', 404
        except Exception as e:
            return str(e), 500 