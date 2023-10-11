from flask_restx import Namespace, Resource
from namespaces.ns_naruc import api
from database import create_connection
from flask import jsonify, request
from models import rating_model
import uuid

# DB Connect
client = create_connection()
db = client['naruc_app']

class RatingsApi(Resource):
    '''
        Endpoint na získanie všetkých ratingov.
    '''
    @api.response(200, 'Success')
    @api.response(404, 'Validation Error')
    def get(self):
        return jsonify(list(db.ratings.find()))
    
    @api.expect(rating_model)
    @api.response(200, 'Successfully Created Question')
    @api.response(404, 'Question Not Found')
    def post(self):
        api.payload['_id'] = uuid.uuid4().hex
        db.ratings.insert_one(api.payload)
        
        return api.payload

# Get rating info by ID
class get_rating_info(Resource):
    @api.doc(description="Get information about a specific rating by ID")
    def get(self, rating_id):
        try:
            rating = db.ratings.find_one({'_id': rating_id})

            if rating:
                return rating, 200
            else:
                return {'message': 'Rating not found'}, 404
        except Exception as e:
            return str(e), 500