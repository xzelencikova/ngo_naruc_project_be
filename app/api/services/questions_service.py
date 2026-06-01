from app.api.db.database import Database
from app.api.db.repositories.questions_repo import QuestionsRepository


class QuestionsService:
    def __init__(self):
        self.engine = Database.get_engine()
        self.repo = QuestionsRepository(engine=self.engine)

    def get_all_questions(self):
        questions_df = self.repo._convert_to_dataframe(self.repo.get_all_questions())
        return self.repo._convert_to_dict(questions_df)

    def create_new_question(self, payload):
        try:
            questions_df = self.repo._convert_to_dataframe(
                self.repo.get_questions_by_category(payload["category"])
            )
            if questions_df.empty:
                payload["category_order"] = self.repo.get_last_category_id()[0]["max"]
                payload["icon"] = "fa-sliders"
            else:
                payload["category_order"] = int(questions_df.loc[0, "category_order"])
                payload["icon"] = questions_df.loc[0, "icon"]

            id = self.repo._load_data_to_db_return_id(
                table_name="questions", data=payload
            )
            return {
                "message": "The question was successfully created.",
                "status": 200,
                "id": id,
            }
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Please, try again later.",
                "status": 500,
            }

    def get_question_by_id(self, id):
        questions_df = self.repo._convert_to_dataframe(self.repo.get_question_by_id(id))
        return self.repo._convert_to_dict(questions_df)[0]

    def update_question_by_id(self, id, payload):
        try:
            payload["id"] = id
            questions_df = self.repo._convert_to_dataframe(
                self.repo.get_questions_by_category(payload["category"])
            )
            if questions_df.empty:
                payload["category_order"] = self.repo.get_last_category_id()[0]["max"]
                payload["icon"] = "fa-sliders"
                print(payload)
            else:
                payload["category_order"] = int(questions_df.loc[0, "category_order"])
                payload["icon"] = questions_df.loc[0, "icon"]
            self.repo._execute_query(self.repo.update_question_by_id(payload))
            return {"message": "The question was successfully updated.", "status": 200}
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Please, try again later.",
                "status": 500,
            }

    def set_question_valid_status(self, payload):
        try:
            self.repo.update_question_valid(ids=payload["lock_questions"], valid=False)
            self.repo.update_question_valid(ids=payload["unlock_questions"], valid=True)
            return {
                "message": "The clients active status was successfully updated.",
                "status": 200,
            }
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Please, try again later.",
                "status": 500,
            }

    def delete_question_by_id(self, id):
        try:
            self.repo.delete_rating_question_by_id(id)
            self.repo.delete_question_by_id(id)
            return {"message": "The question was successfully deleted.", "status": 200}
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Please, try again later.",
                "status": 500,
            }

    def get_all_categories(self):
        categories_df = self.repo._convert_to_dataframe(self.repo.get_all_categories())
        return self.repo._convert_to_dict(categories_df)

    def get_questions_by_category(self):
        questions_df = self.repo._convert_to_dataframe(self.repo.get_all_questions())
        categories = questions_df["category"].unique().tolist()
        questions_df = questions_df[questions_df["is_valid"]]
        results = []

        for category in categories:
            cat_df = questions_df[questions_df["category"] == category]

            results.append(
                {
                    "category": category,
                    "icon": cat_df["icon"].unique().tolist()[0],
                    "category_order": cat_df["category_order"].unique().tolist()[0],
                    "questions": self.repo._convert_to_dict(cat_df[["id", "question"]]),
                }
            )
        return sorted(results, key=lambda x: x["category_order"])
