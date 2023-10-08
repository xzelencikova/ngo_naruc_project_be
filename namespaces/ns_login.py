from flask_restx import Namespace, Resource
from namespaces.ns_naruc import api
from database import create_connection
from flask import request, jsonify
from bson.objectid import ObjectId
import bcrypt
import uuid
from models import login_model, user_model

# DB Connect
client = create_connection()
db = client['naruc_app']

users_collection = db['users']

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
                    'name': user['name'],
                    'surname': user['surname'],
                    'email': user['email'],
                    'role': user['role']
                }
                return user_data, 200
            else:
                return 'Not Found', 404
        except Exception as e:
            return str(e), 500

#add user
class sign_in(Resource):
    @api.doc(description="Create a new user")
    @api.expect(user_model)  # Use the defined model for the expected input
    def post(self):
        # Generate a new unique ID for the user
        user_id = uuid.uuid4().hex

        # Set the '_id' field to the generated user ID
        api.payload['_id'] = user_id
        data = api.payload  # Use api.payload to access the JSON data

        # Hash the password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Create a user data dictionary
        user_data = {
            '_id': user_id,  # Set '_id' to the generated user ID
            'name': data['name'],
            'surname': data['surname'],
            'email': data['email'],
            'role': data['role'],
            'password': hashed_password
        }

        try:
            # Connect to MongoDB and select the 'users' collection
            users_collection = db.users

            # Insert the new user data into the 'users' collection
            users_collection.insert_one(user_data)

            return 'User created', 200
        except Exception as e:
            return str(e), 500 

#get_users 
class get_users(Resource):
    @api.doc(description="Get information about all registered users")
    def get(self):
        try:
            # Find all users, excluding the '_id' and 'password' fields
            users = list(db.users.find({}, {'password': 0}))
            
            if users:
                return users, 200
            else:
                return [], 200  # Return an empty list with a 200 status code if no users are found
        except Exception as e:
            return str(e), 500 

#update_user_info 
class update_user_info(Resource):
     @api.expect(user_model)
     def put(self, user_id):
        data = request.json
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        try:
            result = db.users.update_one({'_id': user_id}, {
                '$set': {
                    'name': data['name'],
                    'surname': data['surname'],
                    'email': data['email'],
                    'role': data['role'],
                    'password': hashed_password
                }
            })
            if result.modified_count == 1:
                return 'User information updated successfully', 200
            else:
                return 'User not found', 404
        except Exception as e:
            return str(e), 500  # Return a 500 status code for server error

# Get user info
class get_user_info(Resource):
    @api.doc(description="Get information about a specific client by ID")
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
    def delete(self, user_id):
        try:
            result = db.users.delete_one({'_id':user_id})
            if result.deleted_count == 1:
                return 'User was deleted', 202
            else:
                return 'User not found', 404
        except Exception as e:
            return str(e), 500 