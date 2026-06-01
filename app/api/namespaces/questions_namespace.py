from flask_restx import Namespace, Resource

from app.api.utils.auth_token import *

from app.api.models.questions_models import register_question_models
from app.api.services.questions_service import QuestionsService

api = Namespace(
    "Questions", description="API for questions operations.", path="/questions"
)

models = register_question_models(api)
service = QuestionsService()


@api.route("")
class GetAllQuestionsEndpoint(Resource):

    @api.doc(description="Get list of all questions.", security="apikey")
    @token_required
    def get(self):
        return service.get_all_questions()

    @api.expect(models["question"])
    @api.doc(description="Create new question.", security="apikey")
    @token_required
    def post(self):
        return service.create_new_question(api.payload)

    @api.expect(models["lock_questions"])
    @api.doc(description="Update questions' valid status", security="apikey")
    @token_required
    def put(self):
        return service.set_question_valid_status(api.payload)


@api.route("/<int:id>")
class GetQuestionByIdEndpoint(Resource):

    @api.doc(description="Get question by id.", security="apikey")
    @token_required
    def get(self, id):
        return service.get_question_by_id(id)

    @api.expect(models["question"])
    @api.doc(description="Update question by id.", security="apikey")
    @token_required
    def put(self, id):
        return service.update_question_by_id(id, api.payload)

    @api.doc(security="apikey")
    @token_required
    def delete(self, id):
        return service.delete_question_by_id(id)


@api.route("/categories")
class GetQuestionsByCategoriesEndpoint(Resource):

    @api.doc(description="Get list of all categories.", security="apikey")
    @token_required
    def get(self):
        return service.get_all_categories()

    @api.doc(description="Get list of all questions by categories.", security="apikey")
    @token_required
    def post(self):
        return service.get_questions_by_category()
