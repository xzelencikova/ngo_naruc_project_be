from flask_restx import Namespace, Resource, reqparse
from database import create_connection
from flask import request, jsonify
from bson.objectid import ObjectId
from datetime import datetime 
import uuid
from models import client_model
from auth_middleware import token_required

api = Namespace('client', description='Client management')

# DB Connect
client = create_connection()
db = client['naruc_app']

users_collection = db['clients']

# Add client
class add_client(Resource):
    @api.doc(description="Create a new client", security="apikey")
    @token_required
    @api.expect(client_model)
    def post(self):
        client_data = api.payload
        client_data['_id'] = uuid.uuid4().hex
        client_data['registration_date'] = datetime.now().strftime('%Y-%m-%d')
         

        try:
            db.clients.insert_one(client_data)
            return client_data, 200
        except Exception as e:
            return str(e), 500

# Get client info
class get_client_info(Resource):
    @api.doc(description="Get information about a specific client by ID", security="apikey")
    @token_required
    def get(self, user_id):
        try:
            clients = db.clients.find_one({'_id': user_id})

            if clients:
                return clients, 200
            else:
                return {'message': 'Client not found'}, 404
        except Exception as e:
            return str(e), 500

# Get clients results/ not working, needs to be fixed later
class get_client_results(Resource):
    @api.doc(description="Get information about a specific client's results", security="apikey")
    @token_required
    def get(self, user_id):
        try:
            ratings = db.ratings.find({"client_id": user_id})
            client_ratings = list(ratings)
            if client_ratings:
                return client_ratings, 200
            else:
                return [], 200
        except Exception as e:
            return str(e), 500
        
# Update client
class update_client_info(Resource):
     @api.expect(client_model)
     @api.doc(security="apikey")
     @token_required
     def put(self, user_id):
        data = request.json
        try:
            result = db.clients.update_one({'_id': user_id}, {
                '$set': {
                    'name': data['name'],
                    'surname': data['surname'],
                    'last_phase': data['last_phase'],
                    'active': data['active']
                }
            })
            if result.modified_count == 1:
                return 'Client information updated successfully', 200
            else:
                return 'Client not found', 404
        except Exception as e:
            return str(e), 500  # Return a 500 status code for server error

# show all clients
class get_clients(Resource):
    @api.doc(description="Get information about all clients", security="apikey")
    @token_required
    def get(self):
        try:
            users = list(db.clients.find())
            
            if users:
                return users, 200
            else:
                return [], 200 
        except Exception as e:
            return str(e), 500 

# Delete client
class delete_client(Resource):
    @api.doc(security="apikey")
    @token_required
    def delete(self, user_id):
        try:
            result = db.clients.delete_one({'_id':user_id})
            if result.deleted_count == 1:
                return 'Client was deleted', 202
            else:
                return 'Client not found', 404
        except Exception as e:
            return str(e), 500 