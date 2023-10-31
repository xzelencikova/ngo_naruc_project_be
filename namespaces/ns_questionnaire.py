from flask_restx import Namespace, Resource
from namespaces.ns_naruc import api
from database import create_connection
from flask import jsonify, request
from models import question_model
import uuid
from auth_middleware import *

# DB Connect
client = create_connection()
db = client['naruc_app']

class QuestionsApi(Resource):
    '''
        Endpoint na získanie všetkých otázok s prislúchajúcimi kategóriami z databázy a vytvorenie novej otázky.
    '''
    
    @api.response(200, 'Success')
    @api.response(404, 'Validation Error')
    @api.doc(security="apikey")
    @token_required
    def get(self):
        
        response = db.questionnaire.find()
        
        questions = [{
            "_id": res['_id'],
            "question": res['question'],
            "category": res['category']
        } for res in response]
        
        return questions
    
    @api.expect(question_model)
    @api.response(200, 'Successfully Created Question')
    @api.response(404, 'Question Not Found')
    @api.doc(security="apikey")
    @token_required
    def post(self):
        api.payload['_id'] = uuid.uuid4().hex
        db.questionnaire.insert_one(api.payload)
        
        return api.payload
    
class QuestionsCategoryApi(Resource):
    '''
        Endpoint na získanie všetkých kategórií s prislúchajúcimi ikonami a zoznamom otázok.
    '''
    
    @api.response(200, 'Success')
    @api.response(404, 'Validation Error')
    @api.doc(security="apikey")
    @token_required
    def get(self):
        
        response = db.questionnaire.find()
        categories = {}
        
        for r in response:
            
            if r['order'] in categories:
                categories[r['order']]["questions"].append({"_id": r['_id'], "question": r['question']})
                continue
            
            categories[r['order']] = {
                "category": r['category'],
                "icon": r['icon'],
                "order": r['order'],
                "questions": [{"_id": r['_id'], "question": r['question']}]
            }
                    
        questions_by_categories = []
        for c in categories:
            questions_by_categories.append(categories[c])
            
        return sorted(questions_by_categories, key=lambda d: d['order'])
    
class QuestionByIdApi(Resource):
    '''
        Endpoint na získanie/aktualizovanie/vymazanie otázky podľa id.
    '''
    
    @api.response(200, 'Question Found')
    @api.response(404, 'Question Not Found')
    @api.doc(security="apikey")
    @token_required
    def get(self, id):
        question = db.questionnaire.find_one({"_id": id})
        return question

    @api.expect(question_model)
    @api.response(200, 'Successfully Updated Question')
    @api.response(404, 'Question Not Found')
    @api.doc(security="apikey")
    @token_required
    def put(self, id):
        question = db.questionnaire.update_one({"_id": id}, {"$set": {"question": api.payload['question'], "category": api.payload['category']}})
        return {"message": "The question was successfully updated."}
    
    @api.response(202, 'Successfully Deleted Question')
    @api.response(404, 'Question Not Found')
    @api.doc(security="apikey")
    @token_required
    def delete(self, id):
        question = db.questionnaire.delete_one({"_id": id})
        return {"message": "The question was successfully deleted."}
