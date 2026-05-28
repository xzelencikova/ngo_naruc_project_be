from app.api.db.repositories.base_repo import BaseRepository, RowList
import app.api.db.data.queries as queries


class ClientsRepository(BaseRepository):
    def get_all_clients(self):
        return self._execute_query(queries.get_all_clients_query())

    def get_client_by_id(self, id):
        params = {"id": id}
        return self._execute_query(queries.get_client_by_id_query(), params=params)

    def set_client_active_status(self, clients, active):
        params = {"clients": clients, "active": active}
        return self._commit(queries.set_client_active_status_query(), params=params)

    def update_client_by_id(self, params):
        return self._commit(queries.update_client_query(), params=params)

    def delete_client_by_id(self, id):
        params = {"id": id}
        return self._commit(queries.delete_client_by_id_query(), params=params)

    def delete_rating_by_client_id(self, id):
        params = {"id": id}
        return self._commit(queries.delete_ratings_by_client_query(), params=params)

    def delete_rating_score_by_client_id(self, id):
        params = {"client_id": id}
        return self._commit(
            queries.delete_ratings_score_for_client_query(), params=params
        )
