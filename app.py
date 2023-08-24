from flask import Flask
from flask_restx import Namespace, Resource, Api
import os
import pandas as pd
from flask_cors import CORS, cross_origin

from namespaces.ns_naruc import api as ngo_naruc
from namespaces.ns_manage_survey import *

port = os.getenv('PORT')

app = Flask(__name__)
api = Api(app)

api.add_namespace(ngo_naruc, path='/ngo')

# Example endpoint
ngo_naruc.add_resource(manage_survey, '/survey')


if __name__ == '__main__':
    
    if port is None:
        app.run(host='localhost', port=5000, debug=True, threaded=True)
    
    else:
        app.run(host='0.0.0.0', port=int(port), debug=False, threaded=True)
