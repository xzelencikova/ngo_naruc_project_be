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
        print(api.payload)
        rating = db.ratings.find_one({"client_id": api.payload["client_id"], "phase_no": api.payload["phase_no"]})
        
        if rating:
            db.ratings.update_one({"_id": rating["_id"]}, {"$set": api.payload})
        else:
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
        
def count_ratings_for_phase(category, questions):
    value = 0
    for q in questions:
        if q["category"] == category:
            value += q["rating"]

    return value
    
# Get rating overview for client
class RatingOverviewApi(Resource):
    
    def get(self, client_id):
        
        response = db.questionnaire.distinct("category")
        overview = {
            "bar_overview": [],
            "pie_1": [],
            "pie_2": [],
            "pie_3": []
        }
        
        for r in response:
            
            phase_1 = 0
            phase_2 = 0
            phase_3 = 0
            
            questions_count = len(list(db.questionnaire.find({"category": r})))
            
            client_ratings = db.ratings.find({"client_id": client_id})

            for c in client_ratings:
                if c["phase_no"] == 1:
                    phase_1 = count_ratings_for_phase(r, c["questions_rating"])
                elif c["phase_no"] == 2:
                    phase_2 = count_ratings_for_phase(r, c["questions_rating"])
                elif c["phase_no"] == 3:
                    phase_3 = count_ratings_for_phase(r, c["questions_rating"])
            
            overview['bar_overview'].append(
                {
                    "name": r,
                    "series": [
                        {
                            "name": "Fáza 1", 
                            "value": round(phase_1 / (questions_count * 3) * 100, 2)
                        },
                        {
                            "name": "Fáza 2", 
                            "value": round(phase_2 / (questions_count * 3) * 100, 2)
                        },
                        {
                            "name": "Fáza 3", 
                            "value": round(phase_3 / (questions_count * 3) * 100, 2)
                        }
                    ]
                })
            overview['pie_1'].append(
                {
                    "name": r,
                    "value": phase_1
                })
            overview['pie_2'].append(
                {
                    "name": r,
                    "value": phase_2
                })
            overview['pie_3'].append(
                {
                    "name": r,
                    "value": phase_3
                })
            
        return overview
        