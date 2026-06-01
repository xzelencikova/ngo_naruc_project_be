import bcrypt
from datetime import datetime, timedelta, timezone
import jwt
import os
import pandas as pd
from typing import Any

from app.api.db.database import Database
from app.api.db.repositories.users_repo import UsersRepository
from app.api.dto.users import UserAuthDTO, UserDTO, UserRegistrationDTO

type RowList = list[dict[str, Any]]


class UsersService:
    def __init__(self):
        self.engine = Database.get_engine()
        self.repo = UsersRepository(engine=self.engine)

    def _encode_auth_token(self, user_id):
        """Generates the Auth Token"""
        try:
            payload = {
                "exp": datetime.now(timezone.utc) + timedelta(days=1),
                "iat": datetime.now(timezone.utc),
                "sub": user_id,
            }
            print(payload)

            return jwt.encode(payload, os.environ.get("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            return e

    def process_auth(self, payload: UserAuthDTO) -> dict[str, Any]:
        try:
            users_df = self.repo._convert_to_dataframe(
                self.repo.get_user_by_email(email=payload["email"])
            )

            if not users_df.empty:
                user = self.repo._convert_to_dict(users_df)[0]
                check_pwd = bcrypt.checkpw(
                    payload["password"].encode("utf-8"),
                    user["password"].encode("utf-8"),
                )

                if check_pwd:
                    user["token"] = self._encode_auth_token(user["id"])
                    del user["password"]
                    return user
            return {
                "message": "Incorrect email or password. The authentication failed.",
                "status": 401,
            }
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Try again later.",
                "status": 500,
            }

    def process_user_registration(
        self, new_user: UserRegistrationDTO
    ) -> dict[str, Any]:
        try:
            new_user["password"] = bcrypt.hashpw(
                new_user["password"].encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            id = self.repo._load_data_to_db_return_id(table_name="users", data=new_user)
            return {
                "message": "New user was successfully created.",
                "status": 200,
                "id": id,
            }
        except Exception as e:
            print(e)
            return {"message": "Something went wrong. Try again later.", "status": 500}

    def get_all_users(self) -> RowList:
        users_df = self.repo._convert_to_dataframe(self.repo.get_all_users())
        return self.repo._convert_to_dict(users_df)

    def get_user_by_id(self, id: int):
        users_df = self.repo._convert_to_dataframe(self.repo.get_user_by_id(id))
        if users_df.empty:
            return {"message": "The user could not be found.", "status": 404}
        users_df = users_df.drop(columns=["password"])
        return self.repo._convert_to_dict(users_df)[0]

    def update_user_password(self, id: int, payload):
        try:
            print(payload)
            hashed_password = bcrypt.hashpw(
                payload["password"].encode("utf-8"), bcrypt.gensalt()
            )
            print(hashed_password)
            self.repo.update_user_password(id, hashed_password.decode("utf-8"))
            return {"message": "The password was successfullly updated.", "status": 200}
        except Exception as e:
            print(e)
            return {"message": "Something went wrong. Try again later.", "status": 500}

    def update_user_by_id(self, payload: UserDTO):
        try:
            rows_updated = self.repo.update_user_by_id(payload)
            return payload
        except Exception as e:
            print(e)
            return {"message": "Something went wrong. Try again later.", "status": 500}

    def delete_user_by_id(self, id: int):
        try:
            rows_deleted = self.repo.delete_user_by_id(id)
            return {
                "message": f"The user with id {id} was successfully deleted.",
                "status": 200,
            }
        except Exception as e:
            print(e)
            return {"message": "Something went wrong. Try again later.", "status": 500}
