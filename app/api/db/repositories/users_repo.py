from app.api.db.repositories.base_repo import BaseRepository, RowList
import app.api.db.data.queries as queries
from app.api.dto.users import UserDTO


class UsersRepository(BaseRepository):

    # Function to get user by email address
    def get_user_by_email(self, email):
        params = {"email": email}
        return self._execute_query(queries.get_user_by_email_query(), params=params)

    def get_all_users(self):
        return self._execute_query(queries.get_all_users_query())

    def get_user_by_id(self, id: int):
        params = {"id": id}
        return self._execute_query(queries.get_user_by_id_query(), params=params)

    def update_user_password(self, id: int, password: str):
        params = {"id": id, "password": password}
        return self._commit(queries.update_user_password_query(), params=params)

    def update_user_by_id(self, params: UserDTO):
        return self._commit(queries.update_user_query(), params=params)

    def delete_user_by_id(self, id: int):
        params = {"id": id}
        return self._commit(queries.delete_user_by_id_query(), params=params)
