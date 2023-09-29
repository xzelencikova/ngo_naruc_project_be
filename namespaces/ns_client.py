from flask_restx import Namespace, Resource, reqparse
from database import create_connection
from flask import request, jsonify
from bson.objectid import ObjectId
import uuid
from models import client_model

api = Namespace('client', description='Client management')

# DB Connect
client = create_connection()
db = client['naruc_app']

users_collection = db['clients']

# Add client
class add_client(Resource):
    @api.doc(description="Create a new client")
    @api.expect(client_model)  
    def post(self):
        user_id = uuid.uuid4().hex

        api.payload['_id'] = user_id
        data = api.payload  

        user_data = {
            '_id': user_id, 
            'name': data['name'],
            'surname': data['surname'],
            'registration_date': data['registration_date'],
            'contract_no': data['contract_no'],
            'last_phase': data['last_phase'],
            'active': data['active']
        }

        try:
            users_collection = db.clients
            users_collection.insert_one(user_data)

            return 'Client created', 200
        except Exception as e:
            return str(e), 500

# Get client info
class get_client_info(Resource):
    @api.doc(description="Get information about a specific client by ID")
    def get(self, user_id):
        try:
            clients = db.clients.find_one({'_id': user_id}, {'_id': 0})

            if clients:
                return clients, 200
            else:
                return {'message': 'Client not found'}, 404
        except Exception as e:
            return str(e), 500

# Get clients results/ not working, needs to be fixed later
class get_client_results(Resource):
    @api.doc(description="Get information about all clients")
    def get(self,user_id):
        try:
            users = list(db.client.find({}, {'_id': 0}))

            if users:
                return users, 200
            else:
                return [], 200  
        except Exception as e:
            return str(e), 500
        
# Update client
class update_client_info(Resource):
     @api.expect(client_model)
     def put(self, user_id):
        data = request.json
        try:
            result = db.clients.update_one({'_id': user_id}, {
                '$set': {
            'name': data['name'],
            'surname': data['surname'],
            'registration_date': data['registration_date'],
            'contract_no': data['contract_no'],
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

# Delete client
class delete_client(Resource):
    def delete(self, user_id):
        try:
            result = db.clients.delete_one({'_id':user_id})
            if result.deleted_count == 1:
                return 'Client was deleted', 202
            else:
                return 'Client not found', 404
        except Exception as e:
            return str(e), 500 