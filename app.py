from flask import Flask
from flask_restx import Namespace, Resource, Api
import os
import pandas as pd
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from dotenv import load_dotenv

from namespaces.ns_naruc import api as ngo_naruc
from namespaces.ns_questions import *
from namespaces.ns_login import *
from namespaces.ns_client import *
from namespaces.ns_ratings import *

load_dotenv()

port = os.getenv('PORT')

client = MongoClient(os.environ.get('MONGODB_URI'))

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_namespace(ngo_naruc, path='/ngo')

# questionnaire endpoints
ngo_naruc.add_resource(QuestionsApi, '/questions')
ngo_naruc.add_resource(QuestionsByCategoryApi, '/questionnaire')
ngo_naruc.add_resource(QuestionByIdApi, "/question/<string:id>")

# ratings endpoints
ngo_naruc.add_resource(RatingsApi, '/ratings')
ngo_naruc.add_resource(RatingsByClientApi, '/ratings/for_client/<int:client_id>')
ngo_naruc.add_resource(RatingApi,'/rating/<rating_id>')
ngo_naruc.add_resource(RatingOverviewApi, '/rating_overview/<int:client_id>')

# user_management endpoints
ngo_naruc.add_resource(login,'/user/login')
ngo_naruc.add_resource(sign_in,'/user/sign_in')
ngo_naruc.add_resource(get_users,'/user/show_users')
ngo_naruc.add_resource(update_user_info,'/user/update_user/<user_id>')
ngo_naruc.add_resource(delete_user,'/user/delete_user/<user_id>')
ngo_naruc.add_resource(get_user_info,'/user/get_user_info/<user_id>') 
ngo_naruc.add_resource(update_user_password,'/user/update_password/<user_id>')

# client_management endpoints
ngo_naruc.add_resource(get_client_info, '/client/get_client_info/<user_id>')
ngo_naruc.add_resource(add_client, '/client/add_new_client')
ngo_naruc.add_resource(update_client_info,'/client/update_client/<user_id>')
ngo_naruc.add_resource(delete_client, '/client/delete_client/<user_id>')
ngo_naruc.add_resource(get_clients, '/clients')

if __name__ == '__main__':
    
    if port is None:
        app.run(host='localhost', port=5000, debug=True, threaded=True)
    
    else:
        app.run(host='0.0.0.0', port=int(port), debug=False, threaded=True)
