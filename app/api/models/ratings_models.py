from flask_restx import fields


def register_ratings_models(api):

    question_rating_model = api.model(
        "RatingsListModel",
        {
            "category": fields.String,
            "icon": fields.String,
            "question_id": fields.String,
            "question": fields.String,
            "rating": fields.Integer,
        },
    )

    rating_model = api.model(
        "RatingModel",
        {
            "id": fields.Integer,
            "last_update_date": fields.Date,
            "last_update_by": fields.String,
            "client_id": fields.String,
            "client": fields.String,
            "phase": fields.Integer,
            "ratings": fields.List(fields.Nested(question_rating_model)),
        },
    )

    return {"rating": rating_model}
