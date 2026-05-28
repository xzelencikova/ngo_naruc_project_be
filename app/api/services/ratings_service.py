from app.api.db.repositories.ratings_repo import RatingsRepository
from app.api.db.database import Database


class RatingsService:
    def __init__(self):
        self.engine = Database.get_engine()
        self.repo = RatingsRepository(engine=self.engine)

    def get_rating_by_id(self, id):
        ratings_df = self.repo._convert_to_dataframe(self.repo.get_rating_by_id(id))
        rating_score_df = self.repo._convert_to_dataframe(
            self.repo.get_rating_score_by_rating_id([id])
        )

        if ratings_df.empty:
            return {}
        rating = self.repo._convert_to_dict(ratings_df)[0]
        rating["ratings"] = self.repo._convert_to_dict(rating_score_df)
        return rating

    def get_ratings_by_client_id(self, client_id):
        ratings_df = self.repo._convert_to_dataframe(
            self.repo.get_ratings_for_client(client_id)
        )

        if ratings_df.empty:
            return {}

        ids = ratings_df["id"].unique().tolist()
        rating_score_df = self.repo._convert_to_dataframe(
            self.repo.get_rating_score_by_rating_id([ids])
        )

        results = self.repo._convert_to_dict(ratings_df)
        for i in ratings_df.index():
            temp_ratings_df = rating_score_df[
                rating_score_df["rating_id"] == ratings_df.loc[i, "id"]
            ]
            results[i]["ratings"] = self.repo._convert_to_dict(temp_ratings_df)

        return results

    def create_new_rating(self, payload):
        try:
            if payload["id"] is not None and payload["id"] != 0:
                self.repo.delete_rating_score_by_id(payload["id"])
                self.repo.update_rating_by_id(
                    payload["id"],
                    payload["last_update_by"],
                    payload["last_update_date"],
                )
            else:
                rating_info = self.repo._convert_to_dataframe(payload)
                self.repo._load_data_to_db(
                    table_name="ratings",
                    df=rating_info[
                        ["phase", "client_id", "last_update_by", "last_update_date"]
                    ],
                )

            ratings_df = self.repo._convert_to_dataframe(payload["ratings"])
            self.repo._load_data_to_db(
                table_name="questions_ratings",
                df=ratings_df[["question_id", "rating_id", "rating"]],
            )
            return {
                "message": "The rating has been successfully inserted.",
                "status": 200,
            }

        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Please, try again later.",
                "status": 500,
            }

    def delete_rating_by_id(self, id):
        try:
            ratings_df = self.repo._convert_to_dataframe(self.repo.get_rating_by_id(id))
            if ratings_df.empty:
                return {
                    "message": "Nothing to delete.",
                    "status": 200,
                }
            client_id = ratings_df.loc[0, "client_id"]
            self.repo.delete_rating_score_by_id(id)
            self.repo.delete_rating_by_id(id)
            self.repo.set_rating_phase(id, client_id)
            return {
                "message": "The rating has been successfully deleted.",
                "status": 200,
            }
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Please, try again later.",
                "status": 500,
            }

    def delete_ratings_by_client_id(self, id):
        try:
            self.repo._commit(self.repo.delete_rating_score_by_client_id(id))
            self.repo._commit(self.repo.delete_rating_by_client_id(id))
            return {
                "message": "The client and its attached ratings have been successfully deleted.",
                "status": 200,
            }
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Please, try again later.",
                "status": 500,
            }
