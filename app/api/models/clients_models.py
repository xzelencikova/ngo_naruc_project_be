from flask_restx import fields


def register_client_models(api):
    client_model = api.model(
        "NewClientModel",
        {
            "name": fields.String,
            "surname": fields.String,
            "registration_date": fields.String,
            "contract_no": fields.String,
            "last_phase": fields.Integer,
            "active": fields.Boolean,
        },
    )

    lock_clients_model = api.model(
        "ActiveClientsModel",
        {
            "lock_clients": fields.List(fields.Integer),
            "unlock_clients": fields.List(fields.Integer),
        },
    )

    return {"client": client_model, "lock_clients": lock_clients_model}
