from app.api.db.database import Database
from app.api.db.repositories.clients_repo import ClientsRepository
from datetime import datetime


class ClientsService:
    def __init__(self):
        self.engine = Database.get_engine()
        self.repo = ClientsRepository(engine=self.engine)

    def get_all_clients(self):
        clients_df = self.repo._convert_to_dataframe(self.repo.get_all_clients())
        clients_df["registration_date"] = clients_df["registration_date"].astype(str)
        return self.repo._convert_to_dict(clients_df)

    def create_new_client(self, payload):
        try:
            payload["registration_date"] = datetime.now().strftime("%Y-%m-%d")

            id = self.repo._load_data_to_db_return_id(
                table_name="clients",
                data=payload,
            )

            return {
                "message": "The client was successfully created.",
                "status": 200,
                "id": id,
            }
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Please, try again later.",
                "status": 500,
            }

    def set_client_active_status(self, payload):
        try:
            self.repo.set_client_active_status(
                clients=payload["lock_clients"], active=False
            )
            self.repo.set_client_active_status(
                clients=payload["unlock_clients"], active=True
            )
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

    def get_client_by_id(self, id):
        clients_df = self.repo._convert_to_dataframe(self.repo.get_client_by_id(id))
        if clients_df.empty:
            return {}
        clients_df["registration_date"] = clients_df["registration_date"].astype(str)
        return self.repo._convert_to_dict(clients_df)[0]

    def update_client_by_id(self, id, payload):
        try:
            payload["id"] = id
            self.repo._execute_query(self.repo.update_client_by_id(payload))
            return {"message": "The client was successfully updated.", "status": 200}
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Please, try again later.",
                "status": 500,
            }

    def delete_client_by_id(self, id):
        try:
            self.repo.delete_rating_score_by_client_id(id)
            self.repo.delete_rating_by_client_id(id)
            self.repo.delete_client_by_id(id)
            return {
                "message": "The client and its attached ratings were successfully deleted.",
                "status": 200,
            }
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong. Please, try again later.",
                "status": 500,
            }
