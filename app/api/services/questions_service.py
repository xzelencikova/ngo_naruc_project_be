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
                pass
            else:
                payload["order"] = questions_df.loc[0, "order"]
                payload["icon"] = questions_df.loc[0, "icon"]
            self.repo._load_data_to_db(
                table_name="questions", df=self.repo._convert_to_dataframe(payload)
            )
            return {"message": "Otázka bola úspešne vytvorená.", "status": 200}
        except Exception as e:
            print(e)
            return {"message": "Nastala chyba. Skúste to znova neskôr.", "status": 500}

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
                pass
            else:
                payload["order"] = questions_df.loc[0, "order"]
                payload["icon"] = questions_df.loc[0, "icon"]
            self.repo._execute_query(self.repo.update_question_by_id(payload))
            return {"message": "Otázka bola úspešne aktualizovaná.", "status": 200}
        except Exception as e:
            print(e)
            return {"message": "Nastala chyba. Skúste to znova neskôr.", "status": 500}

    def delete_question_by_id(self, id):
        try:
            self.repo._commit(self.repo.delete_rating_question_by_id(id))
            self.repo._commit(self.repo.delete_question_by_id(id))
            return {"message": "Otázka bola úspešne odstránená.", "status": 200}
        except Exception as e:
            print(e)
            return {"message": "Nastala chyba. Skúste to znova neskôr.", "status": 500}

    def get_all_categories(self):
        categories_df = self.repo._convert_to_dataframe(self.repo.get_all_categories())
        return self.repo._convert_to_dict(categories_df)

    def get_questions_by_category(self):
        questions_df = self.repo._convert_to_dataframe(self.repo.get_all_questions())
        categories = questions_df["category"].unique().tolist()
        results = []

        for category in categories:
            cat_df = questions_df[questions_df["category"] == category]

            results.append(
                {
                    "category": category,
                    "icon": cat_df["icon"].unique().tolist()[0],
                    "order": cat_df["order"].unique().tolist()[0],
                    "questions": self.repo._convert_to_dict(cat_df[["id", "question"]]),
                }
            )
        return sorted(results, key=lambda x: x["order"])
