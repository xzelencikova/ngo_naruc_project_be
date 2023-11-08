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
client, conn = create_connection()
db = client['naruc_app']
cursor = conn.cursor()
users_collection = db['clients']

# Add client
class ClientsApi(Resource):
    
    @api.doc(description="Get information about all clients", security="apikey")
    @token_required
    def get(self):
        try:
            cursor.execute("""SELECT * FROM clients""")
            clients = [
                {
                    "_id": c[0],
                    "name": c[1],
                    "surname": c[2],
                    "registration_date": c[3],
                    "contract_no": c[4],
                    "last_phase": c[5],
                    "active": c[6]
                } for c in cursor.fetchall()
            ]
            return clients

        except Exception as e:
            return str(e), 500 
    
    @api.doc(description="Create a new client", security="apikey")
    @token_required
    @api.expect(client_model)
    def post(self):
        try:
            api.payload['registration_date'] = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""INSERT INTO clients(name, surname, registration_date, contract_no, last_phase, active)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                            (api.payload["name"], api.payload["surname"], api.payload["registration_date"], api.payload["contract_no"], api.payload["last_phase"], api.payload["active"]))
         
            return api.payload, 200
        except Exception as e:
            return str(e), 500

# Get client info
class ClientByIdApi(Resource):
    
    @api.doc(description="Get information about a specific client by ID", security="apikey")
    @token_required
    def get(self, client_id):
        try:
            cursor.execute("""SELECT * FROM clients WHERE id={}""".format(client_id))
            res = cursor.fetchone()
            if res:
                client = {
                    "_id": res[0],
                    "name": res[1],
                    "surname": res[2],
                    "registration_date": res[3],
                    "contract_no": res[4],
                    "last_phase": res[5],
                    "active": res[6]
                } 
                return client
            else:
                return {'message': 'Client not found'}, 404
        
        except Exception as e:
            return str(e), 500
        
    @api.expect(client_model)
    @api.doc(security="apikey")
    @token_required
    def put(self, client_id):
        try:
            cursor.execute("""UPDATE clients 
                                SET name=%s, surname=%s, registration_date=%s, contract_no=%s, last_phase=%s, active=%s
                                WHERE id=%s""", 
                                (api.payload["name"], api.payload["surname"], api.payload["registration_date"], api.payload["contract_no"], api.payload["last_phase"], api.payload["active"], client_id))
            cursor.commit()
            api.payload["_id"] = client_id
            return api.payload, 200
        except Exception as e:
            return str(e), 500  # Return a 500 status code for server error

    @api.doc(security="apikey")
    @token_required
    def delete(self, client_id):
        try:
            cursor.execute("""DELETE FROM clients WHERE id={}""".format(client_id))
            cursor.commit()
            return {"message": "Client deleted successfully."}, 200
        except Exception as e:
            return str(e), 500 