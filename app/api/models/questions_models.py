from flask_restx import fields


def register_question_models(api):
    question_model = api.model(
        "QuestionModel",
        {
            "question": fields.String,
            "category": fields.String,
            "order": fields.Integer,
            "icon": fields.String,
            "is_valid": fields.Boolean,
        },
    )

    lock_questions_model = api.model(
        "ValidQuestionsModel",
        {
            "lock_questions": fields.List(fields.Integer),
            "unlock_questions": fields.List(fields.Integer),
        },
    )

    return {"question": question_model, "lock_questions": lock_questions_model}
