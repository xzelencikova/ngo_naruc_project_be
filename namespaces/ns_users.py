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

def encode_auth_token(user_id):
    """
    Generates the Auth Token
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
class LoginApi(Resource):
    
    @api.doc(description="Login with email and password")
    @api.expect(login_model)
    def post(self):
        try:
            # DB Connect
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM users WHERE email=%s""", (api.payload["email"],))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(api.payload['password'].encode('utf-8'), bytes(user[2], 'utf-8')):
                user_data = {
                    '_id': user[0],
                    'name': user[3],
                    'surname': user[4],
                    'email': user[1],
                    'role': user[5],
                    'token': encode_auth_token(user[0])
                }
                return user_data, 200
            else:
                return 'Not Found', 404
        except Exception as e:
            return str(e), 500
        finally:
            conn.close()

#add user
class RegisterApi(Resource):
    
    @api.doc(description="Create a new user", security="apikey")
    @token_required
    @api.expect(user_model_signin)
    def post(self):
        # DB Connect
        conn = create_connection()
        cursor = conn.cursor()
        hashed_password = bcrypt.hashpw(api.payload['password'].encode('utf-8'), bcrypt.gensalt())  
        user_data = (api.payload['email'], str(hashed_password)[2:-1], api.payload['name'], api.payload['surname'], api.payload['role'])
        
        try:
            cursor.execute("""INSERT INTO users(email, password, name, surname, role)
	                            VALUES (%s, %s, %s, %s, %s)""", user_data)
            conn.commit()
            return {"message": 'User created'}, 200
        except Exception as e:
            return str(e), 500 
        finally:
            conn.close()

#get_users 
class UsersApi(Resource):
    
    @token_required
    @api.doc(description="Get information about all registered users", security='apikey')
    def get(self):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT id, email, name, surname, role FROM users ORDER BY surname, name ASC""")
            users_res = cursor.fetchall()
            
            if users_res:
                users = [{
                    "_id": user_res[0],
                    "email": user_res[1],
                    "name": user_res[2],
                    "surname": user_res[3],
                    "role": user_res[4]
                } for user_res in users_res]
                
                return users, 200
        except Exception as e:
            return str(e), 500
        finally:
            conn.close() 

#update password
class UserChangePasswordApi(Resource):

    @api.expect(user_password)
    @token_required
    @api.doc(security="apikey")
    def put(self, user_id):
        
        conn = create_connection()
        cursor = conn.cursor()
        data = request.json
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        try:
            cursor.execute("""UPDATE users
	                            SET password=%s
	                            WHERE id=%s""", (str(hashed_password)[2:-1], user_id))
            conn.commit()
            return {'message': 'User password changed successfully'}, 200
            # else:
            #     return {'message': 'User not found'}, 404
        except Exception as e:
            return {'message': 'Server error'}, str(e),500
        finally:
            conn.close()

# Get user info
class UserByIdApi(Resource):
    
    @api.doc(description="Get information about a specific client by ID", security="apikey")
    @token_required
    def get(self, user_id):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM users WHERE id={}""".format(user_id))
            user_res = cursor.fetchone()
            
            if user_res:
                user = {
                    "_id": user_res[0],
                    "email": user_res[1],
                    "name": user_res[3],
                    "surname": user_res[4],
                    "role": user_res[5]
                }
                return user, 200
            else:
                return {"message": "User not Found"}, 404
        except Exception as e:
            return str(e), 500
        finally:
            conn.close()
    
    @api.expect(user_model)
    @token_required
    @api.doc(security="apikey")
    def put(self, user_id):
        data = request.json
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""UPDATE users
	                            SET name=%s, surname=%s, role=%s
	                            WHERE id=%s""", (api.payload["name"], api.payload["surname"], api.payload["role"], user_id))
            conn.commit()
            return {
                    "_id": user_id,
                    "email": api.payload["email"],
                    "name": api.payload["name"],
                    "surname": api.payload["surname"],
                    "role": api.payload["role"]
                    }, 200
        except Exception as e:
            return str(e), 500
        finally:
            conn.close()

    @token_required
    @api.doc(security="apikey")
    def delete(self, user_id):
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM users WHERE id={}""".format(user_id))
            conn.commit()
            return {"message": "User was deleted successfully."}, 200
        except Exception as e:
            return str(e), 500
        finally:
            conn.close()
