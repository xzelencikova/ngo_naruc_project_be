from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from dotenv import load_dotenv
import os

from app.config import Config

from app.api.db.database import Database
from app.api.db.repositories.users_repo import UsersRepository

load_dotenv()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        engine = Database.get_engine()
        repo = UsersRepository(engine=engine)

        token = None
        if "X-API-KEY" in request.headers:
            token = request.headers["X-API-KEY"]

        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized",
            }, 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            users_df = repo._convert_to_dataframe(repo.get_user_by_id(data["sub"]))

            if users_df.empty:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized",
                }, 401

        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
            }, 500

        return f(*args, **kwargs)

    return decorated
