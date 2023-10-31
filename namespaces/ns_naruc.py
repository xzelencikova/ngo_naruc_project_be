from flask_restx import Namespace, Resource, fields

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Namespace('NGO_Naruc', description="Requests for NGO Naruc Project", authorizations=authorizations)