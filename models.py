from flask_restx import fields
from namespaces.ns_naruc import api


question_model = api.model("Question", {
    "question": fields.String,
    "category": fields.String,
    "order": fields.Integer,
    "icon": fields.String
})