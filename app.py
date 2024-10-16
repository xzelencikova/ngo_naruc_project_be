from flask import Flask
from flask_restx import Namespace, Resource, Api
import os
import pandas as pd
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from dotenv import load_dotenv

from namespaces.ns_naruc import api as ngo_naruc
from namespaces.ns_questions import *
from namespaces.ns_users import *
from namespaces.ns_clients import *
from namespaces.ns_ratings import *

load_dotenv()

port = os.getenv('PORT')

#client = MongoClient(os.environ.get('MONGODB_URI'))

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/IIS-PythonApi'
api = Api(app, prefix='/IIS-PythonApi')
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

if __name__ == '__main__':
    
    if port is None:
        app.run(host='localhost', port=5000, debug=True, threaded=True)
    
    else:
        app.run(host='0.0.0.0', port=int(port), debug=False, threaded=True)
