from flask_restx import Namespace, Resource

from app.api.utils.auth_token import token_required

from app.api.models.clients_models import register_client_models
from app.api.services.clients_service import ClientsService

api = Namespace("Clients", description="API for clients management", path="/clients")

# Load client models and service
models = register_client_models(api)
service = ClientsService()


# Add client
@api.route("")
class GetAllClientsEndpoint(Resource):

    @api.doc(description="Get list of all clients.", security="apikey")
    @token_required
    def get(self):
        return service.get_all_clients()

    @api.expect(models["lock_clients"])
    @api.doc(description="Update clients' active status", security="apikey")
    @token_required
    def put(self):
        result = service.set_client_active_status(api.payload)

        if result["status"] == 200:
            return result, 200

        return {"message": result["message"]}, 500

    @api.expect(models["client"])
    @api.doc(description="Create a new client.", security="apikey")
    @token_required
    def post(self):
        result = service.create_new_client(api.payload)

        if result["status"] == 200:
            return result, 200

        return {"message": result["message"]}, 500


# Get client info
@api.route("/<int:id>")
class GetClientByIdEndpoint(Resource):

    @api.doc(description="Get client by id.", security="apikey")
    @token_required
    def get(self, id):
        return service.get_client_by_id(id)

    @api.expect(models["client"])
    @api.doc(description="Update client by id.", security="apikey")
    @token_required
    def put(self, id):
        result = service.update_client_by_id(id, api.payload)

        if result["status"] == 200:
            return result, 200

        return {"message": result["message"]}, 500

    @api.doc(description="Delete client by id.", security="apikey")
    @token_required
    def delete(self, id):
        result = service.delete_client_by_id(id)

        if result["status"] == 200:
            return result, 200

        return {"message": result["message"]}, 500
