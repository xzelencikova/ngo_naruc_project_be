from flask_restx import Namespace, Resource
from namespaces.ns_naruc import api

# DB Connect

# api call example
class manage_survey(Resource):
    
    @api.response(200, 'Success')
    @api.response(404, 'Validation Error')
    def get(self):
        return []
    