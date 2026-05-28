from flask_restx import fields


def register_question_models(api):
    question_model = api.model(
        "QuestionModel",
        {
            "question": fields.String,
            "category": fields.String,
            "order": fields.Integer,
            "icon": fields.String,
        },
    )

    return {
        "question": question_model,
    }
