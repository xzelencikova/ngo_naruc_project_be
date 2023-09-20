from flask import Flask
from flask_restx import Namespace, Resource, Api
import os
import pandas as pd
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from dotenv import load_dotenv

from namespaces.ns_naruc import api as ngo_naruc
from namespaces.ns_questionnaire import *
from namespaces.ns_login import *

load_dotenv()

port = os.getenv('PORT')

client = MongoClient(os.environ.get('MONGODB_URI'))

app = Flask(__name__)
api = Api(app)

api.add_namespace(ngo_naruc, path='/ngo')

# questionnaire endpoints
ngo_naruc.add_resource(get_all_questions, '/questions')
ngo_naruc.add_resource(get_questions_by_category, '/questions_by_category')
ngo_naruc.add_resource(question_by_id, "/question/<string:id>")

# user_management endpoints
ngo_naruc.add_resource(login,'/login')
ngo_naruc.add_resource(sign_in,'/sign_in')
ngo_naruc.add_resource(get_users,'/users')
ngo_naruc.add_resource(update_user_info,'/update_user/<user_id>')
ngo_naruc.add_resource(delete_user,'/user/<user_id>')


if __name__ == '__main__':
    
    if port is None:
        app.run(host='localhost', port=5000, debug=True, threaded=True)
    
    else:
        app.run(host='0.0.0.0', port=int(port), debug=False, threaded=True)
        