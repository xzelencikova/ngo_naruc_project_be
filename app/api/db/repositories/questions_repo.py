from app.api.db.repositories.base_repo import BaseRepository, RowList
import app.api.db.data.queries as queries


class QuestionsRepository(BaseRepository):
    def get_all_questions(self):
        return self._execute_query(queries.get_all_questions_query())

    def get_questions_by_category(self, category: str):
        params = {"category": category}
        return self._execute_query(
            queries.get_questions_by_category_query(), params=params
        )

    def get_all_categories(self):
        return self._execute_query(queries.get_all_categories_query())

    def get_last_category_id(self):
        return self._execute_query(queries.get_max_category_query())

    def get_question_by_id(self, id):
        params = {"id": id}
        return self._execute_query(queries.get_question_by_id_query(), params=params)

    def update_question_by_id(self, params):
        return self._commit(queries.update_question_query(), params=params)

    def delete_question_by_id(self, id):
        params = {"id": id}
        return self._commit(queries.delete_question_by_id_query(), params=params)

    def delete_rating_question_by_id(self, id):
        params = {"id": id}
        return self._commit(
            queries.delete_ratings_score_by_question_id(), params=params
        )
