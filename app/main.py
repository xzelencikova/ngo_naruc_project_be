from flask import Flask, Blueprint
from flask_restx import Api
from flask_restx.apidoc import apidoc
import os
from flask_cors import CORS, cross_origin

from app.config import Config
from app.api.db.database import Database

cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cors.init_app(app)

    Database.init(Config.DATABASE_URL)

    authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "X-API-KEY"}}

    api_bp = Blueprint(
        "api",
        __name__,
        url_prefix=os.environ.get("API_ROOT") + os.environ.get("API_SUFFIX"),
    )
    api = Api(
        api_bp,
        version="1.0",
        title="NGO Naruc BackEnd API UI",
        description="Welcome to Flask-RESTX API with Swagger UI documentation",
        doc=os.environ.get("API_SWAGGERUI"),
        authorizations=authorizations,
        security="apikey",
    )
    apidoc.static_url_path = os.environ.get("API_ROOT") + "/swaggerui"
    app.register_blueprint(api_bp)

    from app.api.namespaces.questions_namespace import api as questions_ns
    from app.api.namespaces.users_namespace import api as users_ns
    from app.api.namespaces.clients_namespace import api as clients_ns
    from app.api.namespaces.ratings_namespace import api as ratings_ns

    api.add_namespace(questions_ns)
    api.add_namespace(users_ns)
    api.add_namespace(clients_ns)
    api.add_namespace(ratings_ns)

    return app
