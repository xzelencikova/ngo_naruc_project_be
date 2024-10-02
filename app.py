from flask import Flask, Blueprint
from flask_restx import Namespace, Resource, Api
from flask_restx.apidoc import apidoc
import os
import pandas as pd
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from dotenv import load_dotenv
import customLogging
import sys

from namespaces.ns_naruc import api as ngo_naruc
from namespaces.ns_questions import *
from namespaces.ns_users import *
from namespaces.ns_clients import *
from namespaces.ns_ratings import *

scriptName = os.path.basename(__file__)
scriptFolder = os.path.dirname(__file__)

logging = customLogging.setupCustomLogging(scriptName)

logging.info(scriptName + '| ------------------------------------------------------------')
logging.info(scriptName + '| Script name: [' + scriptName + ']')

# Determine if the application is a script file or a frozen executable file
if getattr(sys, 'frozen', False):
    scriptFolder = os.path.dirname(sys.executable)
    logging.debug(scriptName + '| Application was launched from frozen executable located in: [' + scriptFolder + ']')
    scriptFolder = os.path.dirname(__file__)
    logging.debug(scriptName + '| Extracted temp files location from the frozen executable: [' + scriptFolder + ']')
elif __file__:
    scriptFolder = os.path.dirname(__file__)
    logging.debug(scriptName + '| Application was launched from python script located in: [' + scriptFolder + ']')
logging.info(scriptName + '| Application folder: [' + scriptFolder + ']')

load_dotenv()

port = int(os.environ.get('SERVER_PORT', '5555')) # debug port when app is run directly

client = MongoClient(os.environ.get('MONGODB_URI'))

app = Flask(__name__)
api_bp = Blueprint(
    'api',
    __name__,
    url_prefix=os.environ.get('API_ROOT') + os.environ.get('API_SUFFIX')
)
api = Api(
    api_bp,
    version='1.0',
    title='NGO Naruc BackeEnd API UI',
    description='Welcome to Flask-RESTX API with Swagger UI documentation',
    doc=os.environ.get('API_SWAGGERUI'),
)
apidoc.static_url_path=os.environ.get('API_ROOT') + "/swaggerui"
app.register_blueprint(api_bp)
CORS(app)

api.add_namespace(ngo_naruc, path='/ngo')

# questionnaire endpoints
ngo_naruc.add_resource(QuestionsApi, '/questions')
ngo_naruc.add_resource(CategoriesApi, '/categories')
ngo_naruc.add_resource(QuestionsByCategoryApi, '/questionnaire')
ngo_naruc.add_resource(QuestionByIdApi, "/question/<int:id>")

# ratings endpoints
ngo_naruc.add_resource(RatingsApi, '/ratings')
ngo_naruc.add_resource(RatingsByClientApi, '/ratings/for_client/<int:client_id>')
ngo_naruc.add_resource(RatingApi,'/rating/<rating_id>')
ngo_naruc.add_resource(RatingOverviewApi, '/rating_overview/<int:client_id>')

# user_management endpoints
ngo_naruc.add_resource(LoginApi,'/user/login')
ngo_naruc.add_resource(RegisterApi,'/user/register')
ngo_naruc.add_resource(UsersApi,'/users')
ngo_naruc.add_resource(UserByIdApi,'/user/<int:user_id>') 
ngo_naruc.add_resource(UserChangePasswordApi,'/user/update_password/<user_id>')

# client_management endpoints
ngo_naruc.add_resource(ClientByIdApi, '/client/<int:client_id>')
ngo_naruc.add_resource(ClientsApi, '/clients')

# DEBUG API ENDPOINT: http://localhost:5555/ngo_naruc_project_be/api/v1/hello
# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}

if __name__ == '__main__':
    if port is None:
        app.run(host='localhost', port=5000, debug=True, threaded=True)
    
    else:
        app.run(host='0.0.0.0', port=int(port), debug=False, threaded=True)
