from flask_restx import Namespace, Resource

from app.api.utils.auth_token import token_required

from app.api.models.ratings_models import register_ratings_models
from app.api.services.ratings_service import RatingsService

api = Namespace("Ratings", description="API for ratings management.", path="/ratings")

models = register_ratings_models(api)
service = RatingsService()


@api.route("")
class CreateRatingsEndpoint(Resource):

    @api.expect(models["rating"])
    @api.doc(description="Create new rating.", security="apikey")
    @token_required
    def post(self):
        return service.create_new_rating(api.payload)


# Get rating info by ID
@api.route("/<int:id>")
class GetRatingByIdEndpoint(Resource):

    @api.doc(description="Get rating by id.", security="apikey")
    @token_required
    def get(self, id):
        return service.get_rating_by_id(id)

    @api.doc(
        description="Delete rating by id.",
        security="apikey",
    )
    @token_required
    def delete(self, id):
        return service.delete_rating_by_id(id)


# Get clients results/ not working, needs to be fixed later
@api.route("/client-id/<int:id>")
class GetRatingsByClientEndpoint(Resource):

    @api.doc(
        description="Get rating by client id.",
        security="apikey",
    )
    @token_required
    def get(self, id):
        return service.get_ratings_by_client_id(id)

    @api.doc(
        description="Delete all client results.",
        security="apikey",
    )
    @token_required
    def delete(self, id):
        return service.delete_ratings_by_client_id(id)
