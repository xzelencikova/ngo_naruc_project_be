from flask_restx import fields
from namespaces.ns_naruc import api

datetime_format = "%Y-%m-%d"

question_model = api.model("Question", {
    "question": fields.String,
    "category": fields.String,
    "order": fields.Integer,
    "icon": fields.String
})

user_model = api.model("Login User", {
    "name": fields.String,
    "surname": fields.String,
    "email": fields.String,
    "role": fields.String,
    "password": fields.String
})

login_model = api.model("Login Data", {
    "email": fields.String(required=True, description="User email"),
    "password": fields.String(required=True, description="User password")
})

question_rating_model = api.model("Question Rating", {
    "question_id": fields.String,
    "question": fields.String,
    "rating": fields.Integer,
    "category": fields.String,
    "icon": fields.String
})

rating_model = api.model("Rating", {
    "date_rated": fields.Date,
    "rated_by_user_id": fields.String,
    "client_id": fields.String,
    "phase_no": fields.Integer,
    "questions_rating": fields.List(fields.Nested(question_rating_model))
})

client_model = api.model("Add client", {
    "name": fields.String,
    "surname": fields.String,
    "registration_date": fields.DateTime(dt_format=datetime_format),
    "contract_no": fields.String,
    "last_phase": fields.String,
    "active": fields.Boolean
})
