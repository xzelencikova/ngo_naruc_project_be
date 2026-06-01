import app.api.db.data.queries as queries
from app.api.db.repositories.base_repo import BaseRepository, RowList


class RatingsRepository(BaseRepository):
    # def get_all_ratings(self):
    #     return self._execute_query(queries.get())

    def get_rating_by_id(self, id):
        params = {"id": id}
        return self._execute_query(queries.get_rating_by_id_query(), params=params)

    def get_rating_score_by_rating_id(self, id):
        params = {"rating_ids": id}
        return self._execute_query(
            queries.get_rating_score_by_rating_id_query(), params=params
        )

    def get_ratings_for_client(self, client_id):
        params = {"client_id": client_id}
        return self._execute_query(
            queries.get_ratings_for_client_query(), params=params
        )

    def set_rating_phase(self, id, client):
        params = {"id": id, "client_id": client}
        return self._commit(queries.update_rating_phase_query(), params=params)

    def update_rating_by_id(self, id, update_by, update_date):
        params = {
            "id": id,
            "last_update_by": update_by,
            "last_update_date": update_date,
        }
        return self._commit(queries.update_rating_by_id_query(), params=params)

    def delete_rating_by_id(self, id):
        params = {"id": id}
        return self._commit(queries.delete_rating_info_by_id_query(), params=params)

    def delete_rating_score_by_id(self, id):
        params = {"rating_id": id}
        return self._commit(
            queries.delete_ratings_score_by_rating_id_query(), params=params
        )

    def delete_rating_by_client_id(self, id):
        params = {"id": id}
        return self._commit(queries.delete_ratings_by_client_query(), params=params)

    def delete_rating_score_by_client_id(self, id):
        params = {"client_id": id}
        return self._commit(
            queries.delete_ratings_score_for_client_query(), params=params
        )
