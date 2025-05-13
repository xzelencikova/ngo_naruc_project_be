from flask_restx import Namespace, Resource, reqparse
from database import create_connection
from flask import request, jsonify
from bson.objectid import ObjectId
from datetime import datetime 
import uuid
from models import client_model, lock_clients_model
from auth_middleware import token_required
from namespaces.ns_naruc import api

# Add client
class ClientsApi(Resource):
    
    @api.doc(description="Get information about all clients", security="apikey")
    @token_required
    def get(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM clients ORDER BY id DESC""")
            clients = [
                {
                    "_id": c[0],
                    "name": c[1],
                    "surname": c[2],
                    "registration_date": c[3].strftime("%Y-%m-%d"),
                    "contract_no": c[4],
                    "last_phase": c[5],
                    "active": c[6]
                } for c in cursor.fetchall()
            ]
            return clients

        except Exception as e:
            return str(e), 500 
        finally:
            conn.close()
    
    @api.doc(description="Lock / unlock clients", security="apikey")
    @token_required
    @api.expect(lock_clients_model)
    def put(self):
        try:
            lock_clients = ", ".join([str(id) for id in api.payload["lock_clients"]])
            unlock_clients = ", ".join([str(id) for id in api.payload["unlock_clients"]])

            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""UPDATE clients
                                SET active=false
                                WHERE id in ({})""".format(lock_clients))
            
            cursor.execute("""UPDATE clients
                                SET active=true
                                WHERE id in ({})""".format(unlock_clients))
            conn.commit()
            conn.close()
         
            return 200
        except Exception as e:
            return str(e), 500
       
            
    @api.doc(description="Create a new client", security="apikey")
    @token_required
    @api.expect(client_model)
    def post(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            api.payload['registration_date'] = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""INSERT INTO clients(name, surname, registration_date, contract_no, last_phase, active)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                RETURNING id""", 
                            (api.payload["name"], api.payload["surname"], api.payload["registration_date"], api.payload["contract_no"], api.payload["last_phase"], api.payload["active"]))
            id = cursor.fetchone()
            api.payload["_id"] = id[0]
            conn.commit()
         
            return api.payload, 200
        except Exception as e:
            return str(e), 500
        finally:
            conn.close()

# Get client info
class ClientByIdApi(Resource):
    
    @api.doc(description="Get information about a specific client by ID", security="apikey")
    @token_required
    def get(self, client_id):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM clients WHERE id={}""".format(client_id))
            res = cursor.fetchone()
            if res:
                client = {
                    "_id": res[0],
                    "name": res[1],
                    "surname": res[2],
                    "registration_date": datetime.strftime(res[3], "%Y-%m-%d"),
                    "contract_no": res[4],
                    "last_phase": res[5],
                    "active": res[6]
                } 
                return client
            else:
                return {'message': 'Client not found'}, 404
        
        except Exception as e:
            return str(e), 500
        finally:
            conn.close()
        
    @api.expect(client_model)
    @api.doc(security="apikey")
    @token_required
    def put(self, client_id):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""UPDATE clients 
                                SET name=%s, surname=%s, registration_date=%s, contract_no=%s, last_phase=%s, active=%s
                                WHERE id=%s""", 
                                (api.payload["name"], api.payload["surname"], datetime.strptime(api.payload["registration_date"], "%Y-%m-%d"), api.payload["contract_no"], api.payload["last_phase"], api.payload["active"], client_id))
            conn.commit()
            api.payload["_id"] = client_id
            return api.payload, 200
        except Exception as e:
            return str(e), 500  # Return a 500 status code for server error
        finally:
            conn.close()

    @api.doc(security="apikey")
    @token_required
    def delete(self, client_id):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            print(client_id)
            cursor.execute("""DELETE FROM questions_ratings WHERE rating_id in (select id FROM ratings WHERE client_id={})""".format(client_id))
            cursor.execute("""DELETE FROM ratings WHERE client_id={}""".format(client_id))
            cursor.execute("""DELETE FROM clients WHERE id={}""".format(client_id))
            conn.commit()
            return {"message": "Client was deleted successfully."}, 200
        except Exception as e:
            return str(e), 500 
        finally:
            conn.close()