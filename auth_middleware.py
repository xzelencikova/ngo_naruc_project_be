from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
import models
from dotenv import load_dotenv
import os
from database import create_connection

load_dotenv()
conn = create_connection()
cursor = conn.cursor()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "X-API-KEY" in request.headers:
            token = request.headers["X-API-KEY"]
            
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            
        try:
            data = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
            cursor.execute("""SELECT * FROM users WHERE id={}""".format(data["sub"]))
            current_user = cursor.fetchone()
            
            if not current_user:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
                
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(*args, **kwargs)

    return decorated