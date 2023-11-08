from flask_restx import Namespace, Resource
from namespaces.ns_naruc import api
from database import create_connection
from flask import jsonify, request
from models import rating_model
import uuid
import pandas as pd
from auth_middleware import token_required

# DB Connect
client, conn = create_connection()
cursor = conn.cursor()
db = client['naruc_app']

class RatingsApi(Resource):
    '''
        Endpoint na získanie všetkých ratingov.
    '''
    @api.response(200, 'Success')
    @api.response(404, 'Validation Error')
    @api.doc(security="apikey")
    @token_required
    def get(self):
        ratings = []
        ratings_df = pd.read_sql_query("""SELECT r.*, q.id as question_id, q.*, qr.rating FROM ratings r
                            LEFT JOIN questions_ratings qr ON qr.rating_id = r.id
                            RIGHT JOIN questions q ON qr.question_id = q.id
                            ORDER BY r.client_id, r.phase, q.id ASC""", conn)
        clients = ratings_df['client_id'].unique().tolist()
        
        for client in clients:
            phases = ratings_df['phase'].unique().tolist()
            for phase in phases:
                temp_df = ratings_df[(ratings_df['client_id']) == (client & ratings_df['phase'] == phase)]
                ratings.append({
                    "_id": temp_df["id"].tolist()[-1],
                    "phase_no": temp_df["phase"].tolist()[-1],
                    "date_rated": temp_df["last_update_date"].tolist()[-1],
                    "rated_by_user_id": temp_df["last_update_by"].tolist()[-1],
                    "client_id": temp_df["client_id"].tolist()[-1],
                    "questions_rating": temp_df[temp_df.columns[5:]].to_dict('records')
                })
        
        return ratings
    
    @api.expect(rating_model)
    @api.response(200, 'Successfully Created Question')
    @api.response(404, 'Question Not Found')
    @api.doc(security="apikey")
    @token_required
    def post(self):
        ratings_df = pd.read_sql_query("""SELECT r.*, q.id as question_id, q.id as _id, q.category, q.question, q.category_order, q.icon, qr.rating FROM ratings r
                            LEFT JOIN questions_ratings qr ON qr.rating_id = r.id
                            RIGHT JOIN questions q ON qr.question_id = q.id
                            WHERE r.client_id = {} AND r.phase_no = {}
                            ORDER BY r.client_id, r.phase, q.id ASC""".format(api.payload["client_id"], api.payload["phase_no"]), conn)
        
        if not ratings_df.empty:
            rating_id = ratings_df["id"].unique().tolist()[0]
            cursor.execute("""INSERT INTO ratings(phase, client_id, last_update_by, last_update_date)
	                            VALUES (%s, %s, %s, %s, %s)""", (api.payload["phase_no"], api.payload["client_id"], api.payload["rated_by_user_id"], api.payload["date_rated"]))

            for q in api.payload["questions_rating"]:
                if ratings_df[ratings_df['_id'] == api.payload[q['_id']]].empty:
                    cursor.execute("""INSERT INTO questions_ratings(question_id, rating_id, rating)
	                            VALUES (%s, %s, %s)""", (q["_id"], rating_id, api.payload["rating"]))
                else:
                    cursor.execute("""UPDATE questions_ratings
                                   SET question_id=%s, rating_id=%s, rating=%s
                                   WHERE question_id=%s""", (q["_id"], rating_id, api.payload["rating"], q["_id"]))

        else:
            cursor.execute("""INSERT INTO ratings(phase, client_id, last_update_by, last_update_date)
	                        VALUES (%s, %s, %s, %s)""", (api.payload["phase_no"], api.payload["client_id"], api.payload['rated_by_user_id'], api.payload['date_rated']))
            api.payload['_id'] = cursor.fetchone()
            
            for q in api.payload["questions_rating"]:
                cursor.execute("""INSERT INTO questions_ratings(question_id, rating_id, rating)
	                            VALUES (%s, %s, %s)""", (q["_id"], api.payload["_id"],api.payload["rating"]))

        conn.commit()
        return api.payload

# Get rating info by ID
class RatingApi(Resource):
    @api.doc(description="Get information about a specific rating by ID", security="apikey")
    @token_required
    def get(self, rating_id):
        try:
            ratings_df = pd.read_sql_query("""SELECT r.*, q.id as _id, q.category, q.question, q.category_order, q.icon, qr.rating FROM ratings r
                            LEFT JOIN questions_ratings qr ON qr.rating_id = r.id
                            RIGHT JOIN questions q ON qr.question_id = q.id
                            WHERE r.id = {}
                            ORDER BY r.client_id, r.phase, q.id ASC""".format(rating_id), conn)
            
            rating = {}
            if not ratings_df.empty:
                rating = {
                        "_id": ratings_df["id"].tolist()[-1],
                        "phase_no": ratings_df["phase"].tolist()[-1],
                        "date_rated": ratings_df["last_update_date"].tolist()[-1],
                        "rated_by_user_id": ratings_df["last_update_by"].tolist()[-1],
                        "client_id": ratings_df["client_id"].tolist()[-1],
                        "questions_rating": ratings_df[ratings_df.columns[5:]].to_dict('records')
                    }
                return rating, 200
            else:
                return {'message': 'Rating not found'}, 404
        except Exception as e:
            return str(e), 500
    
# Get rating overview for client
class RatingOverviewApi(Resource):
    
    @api.doc(security="apikey")
    @token_required
    def get(self, client_id):
        ratings_df = pd.read_sql_query("""SELECT r.*, q.id as _id, q.category, q.question, q.category_order, q.icon, qr.rating FROM ratings r
                            LEFT JOIN questions_ratings qr ON qr.rating_id = r.id
                            RIGHT JOIN questions q ON qr.question_id = q.id
                            WHERE q.id={}
                            ORDER BY q.id ASC""".format(client_id), conn)
        categories = ratings_df['category'].unique().tolist()
        
        overview = {
            "bar_overview": [],
            "pie_1": [],
            "pie_2": [],
            "pie_3": []
        }
        
        for c in categories:
            
            phase_1 = 0
            phase_2 = 0
            phase_3 = 0
            
            questions_count = ratings_df[ratings_df["category"] == c].shape[0]

            phase_1 = ratings_df[(ratings_df["category"] == c) & (ratings_df["phase"] == 1)]["rating"].sum()
            phase_2 = ratings_df[(ratings_df["category"] == c) & (ratings_df["phase"] == 2)]["rating"].sum()
            phase_3 = ratings_df[(ratings_df["category"] == c) & (ratings_df["phase"] == 3)]["rating"].sum()
            
            overview['bar_overview'].append(
                {
                    "name": c,
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
                    "name": c,
                    "value": phase_1
                })
            overview['pie_2'].append(
                {
                    "name": c,
                    "value": phase_2
                })
            overview['pie_3'].append(
                {
                    "name": c,
                    "value": phase_3
                })
            
        return overview

# Get clients results/ not working, needs to be fixed later
class RatingsByClientApi(Resource):
    @api.doc(description="Get information about a specific client's results", security="apikey")
    @token_required
    def get(self, client_id):
        try:
            ratings = []
            ratings_df = pd.read_sql_query("""SELECT r.*, q.id as question_id, q.*, qr.rating FROM ratings r
                                LEFT JOIN questions_ratings qr ON qr.rating_id = r.id
                                RIGHT JOIN questions q ON qr.question_id = q.id
                                WHERE q.id={}
                                ORDER BY r.client_id, r.phase, q.id ASC""".format(client_id), conn)
            
            phases = ratings_df['phase'].unique().tolist()
            for phase in phases:
                temp_df = ratings_df[ratings_df['phase'] == phase]
                ratings.append({
                    "_id": temp_df["id"].tolist()[-1],
                    "phase_no": temp_df["phase"].tolist()[-1],
                    "date_rated": temp_df["last_update_date"].tolist()[-1],
                    "rated_by_user_id": temp_df["last_update_by"].tolist()[-1],
                    "client_id": temp_df["client_id"].tolist()[-1],
                    "questions_rating": temp_df[temp_df.columns[5:]].to_dict('records')
                })
        
            return ratings, 200
        except Exception as e:
            return str(e), 500