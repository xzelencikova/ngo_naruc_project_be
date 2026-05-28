from flask_restx import Namespace, Resource

from app.api.utils.auth_token import token_required

from app.api.models.users_models import register_user_models
from app.api.services.users_service import UsersService

api = Namespace(
    "Users",
    description="API for users management and user authentication.",
    path="/users",
)

models = register_user_models(api)
service = UsersService()


# Authentication of the user
@api.route("/auth")
class AuthenticationEndpoint(Resource):

    @api.doc(description="Authenticate a user.")
    @api.doc(security=None)
    @api.expect(models["login"])
    def post(self):
        return service.process_auth(payload=api.payload)


# Registration of a new user
@api.route("/registration")
class RegistrationEndpoint(Resource):

    @api.doc(description="Create new user account.", security="apikey")
    @token_required
    @api.expect(models["signup"])
    def post(self):
        return service.process_user_registration(new_user=api.payload)


# get_users
@api.route("")
class GetAllUsersEndpoint(Resource):

    @token_required
    @api.doc(description="Get lidt of all users", security="apikey")
    def get(self):
        return service.get_all_users()


# update password
@api.route("/<int:id>/update-password")
class UpdateUserPasswordEndpoint(Resource):

    @api.expect(models["password"])
    @token_required
    @api.doc(description="Update user password.", security="apikey")
    def put(self, id):
        return service.update_user_password(id, api.payload)


# Get user info
@api.route("/<int:id>")
class GetUserByIdEndpoint(Resource):

    @api.doc(description="Get user by id.", security="apikey")
    @token_required
    def get(self, id: int):
        return service.get_user_by_id(id)

    @api.expect(models["user"])
    @token_required
    @api.doc(description="Update user by id.", security="apikey")
    def put(self, id: int):
        api.payload["id"] = id
        return service.update_user_by_id(api.payload)

    @token_required
    @api.doc(description="Delete user by id.", security="apikey")
    def delete(self, id: int):
        return service.delete_user_by_id(id)
