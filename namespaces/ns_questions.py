from flask_restx import Namespace, Resource
from namespaces.ns_naruc import api
from database import create_connection
from flask import jsonify, request
from models import question_model
import uuid
from auth_middleware import *

# DB Connect
client, conn = create_connection()
cursor = conn.cursor()

class QuestionsApi(Resource):
    '''
        Endpoint na získanie všetkých otázok s prislúchajúcimi kategóriami z databázy a vytvorenie novej otázky.
    '''
    
    @api.response(200, 'Success')
    @api.response(404, 'Validation Error')
    @api.doc(security="apikey")
    @token_required
    def get(self):
        cursor.execute('''SELECT id, question, category FROM questions''')
        results = cursor.fetchall()
        
        questions = [{
                "_id": res[0],
                "question": res[1],
                "category": res[2]
            } for res in results]
        
        return questions
    
    @api.expect(question_model)
    @api.response(200, 'Successfully Created Question')
    @api.response(404, 'Unable to create question')
    @api.doc(security="apikey")
    @token_required
    def post(self):
        try:
            cursor.execute("""SELECT * FROM questions WHERE category='{}'""".format(api.payload['category']))
            category_res = cursor.fetchone()
            
            if category_res:
                api.payload["order"] = category_res[3]
                api.payload["icon"] = category_res[4]
            else:
                cursor.execute("""SELECT MAX(category_order) FROM questions""")
                api.payload["order"] = cursor.fetchone()[0] + 1
            
            cursor.execute("""INSERT INTO questions(
                                category, question, category_order, icon)
                            VALUES (%s, %s, %s, %s)
                            RETURNING id""", (api.payload['category'], api.payload['question'], api.payload['order'], api.payload['icon']))
            
            id = cursor.fetchone()
            api.payload['_id'] = id[0]
            conn.commit()
                    
            return api.payload, 200
        except Exception as e:
            print(e)
            return 404, {"message": "Unable to create question"}

    
class QuestionsByCategoryApi(Resource):
    '''
        Endpoint na získanie všetkých kategórií s prislúchajúcimi ikonami a zoznamom otázok.
    '''
    
    @api.response(200, 'Success')
    @api.response(404, 'Validation Error')
    @api.doc(security="apikey")
    @token_required
    def get(self):
        cursor.execute('''SELECT * FROM questions''')
        categories = {}
        
        for r in cursor.fetchall():
            if r[3] in categories:
                categories[r[3]]["questions"].append({"_id": r[0], "question": r[2]})
                continue
            
            categories[r[3]] = {
                "category": r[1],
                "icon": r[4],
                "order": r[3],
                "questions": [{"_id": r[0], "question": r[2]}]
            }
                    
        questions_by_categories = []
        
        for c in categories:
            questions_by_categories.append(categories[c])
            
        return sorted(questions_by_categories, key=lambda d: d['order']), 200
    
class QuestionByIdApi(Resource):
    '''
        Endpoint na získanie/aktualizovanie/vymazanie otázky podľa id.
    '''
    
    @api.response(200, 'Question Found')
    @api.response(404, 'Question Not Found')
    @api.doc(security="apikey")
    @token_required
    def get(self, id):
        cursor.execute('''SELECT * FROM questions WHERE id=%s''', (id,))
        q = cursor.fetchone()
        
        if q:        
            question = {
                "_id": q[0],
                "question": q[2],
                "category": q[1]
            }
            return question, 200
        else:
            return 404, {"message": "Question not found."}

    @api.expect(question_model)
    @api.response(200, 'Successfully Updated Question')
    @api.response(404, 'Question Not Found')
    @api.doc(security="apikey")
    @token_required
    def put(self, id):
        try:
            cursor.execute("""SELECT * FROM questions WHERE category=%s""", (api.payload['category'],))
            category_res = cursor.fetchone()
            
            if category_res:
                api.payload["order"] = category_res[3]
                api.payload["icon"] = category_res[4]
            else:
                cursor.execute("""SELECT MAX(category_order) FROM questions""")
                api.payload["order"] = cursor.fetchone()[0] + 1
            
            cursor.execute("""UPDATE questions
                                SET category=%s, question=%s, category_order=%s, icon=%s
                                WHERE id=%s""", (api.payload['category'], api.payload['question'], api.payload['order'], api.payload['icon'], id))
            conn.commit()
            
            return api.payload, 200
        except Exception as e:
            print(e)
            return {"message": "Unable to update a question."}, 404
    
    @api.response(200, 'Successfully Deleted Question')
    @api.response(404, 'Question Not Found')
    @api.doc(security="apikey")
    @token_required
    def delete(self, id):
        try:
            cursor.execute("""DELETE FROM questions WHERE id=%s""", (id,))
            conn.commit()
            return {"message": "The question was successfully deleted."}, 200
        except Exception as e:
            print(e)
            return {"message": "Unable to delete question."}, 404
    