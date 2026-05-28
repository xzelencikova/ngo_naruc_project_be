from flask_restx import fields


def register_user_models(api):
    login_model = api.model(
        "AuthModel",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True),
        },
    )

    user_model = api.model(
        "UserModel",
        {
            "name": fields.String,
            "surname": fields.String,
            "email": fields.String,
            "role": fields.String,
        },
    )

    user_signin_model = api.model(
        "UserRegistrationModel",
        {
            "name": fields.String,
            "surname": fields.String,
            "email": fields.String,
            "role": fields.String,
            "password": fields.String,
        },
    )

    password_model = api.model(
        "UserPasswordModel",
        {
            "password": fields.String,
        },
    )

    return {
        "login": login_model,
        "user": user_model,
        "signup": user_signin_model,
        "password": password_model,
    }
