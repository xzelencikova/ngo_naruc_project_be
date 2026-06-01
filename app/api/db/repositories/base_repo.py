import pandas as pd
import sqlalchemy as sa
from sqlalchemy.sql.elements import TextClause, Literal
from typing import Any

from app.api.db.database import Database

type RowList = list[dict[str, Any]]


class BaseRepository:
    def __init__(self, engine):
        self.engine = engine

    def _convert_to_dataframe(self, data: list[dict]) -> pd.DataFrame:
        return pd.DataFrame(data)

    def _convert_to_dict(self, df: pd.DataFrame) -> RowList:
        return df.to_dict(orient="records")

    def _load_data_to_db_return_id(self, table_name: str, data: dict):
        table = Database.get_table(table_name)
        stmt = sa.insert(table).returning(getattr(table.c, "id"))

        with self.engine.begin() as conn:
            result = conn.execute(stmt, data)
            return result.scalar()

    def _bulk_load_data_to_db(
        self,
        table_name: str,
        df: pd.DataFrame,
        index: bool = False,
        if_exists: Literal["fail", "append", "replace"] = "append",
    ) -> int:
        """Bulk insert using pandas. Return number of rows inserted."""
        if df.empty:
            return 0

        df.to_sql(
            name=table_name,
            con=self.engine,
            if_exists=if_exists,
            index=index,
            method="multi",
        )
        return len(df)

    def _execute_query(self, query: TextClause, params=None):
        if isinstance(query, str):
            query = sa.text(query)

        with self.engine.begin() as conn:
            result = conn.execute(query, params or {})
            return result.mappings().all()

    def _commit(self, query: TextClause, params=None):
        """INSERT/UPDATE/DELETE queries that must be committed"""
        if isinstance(query, str):
            query = sa.text(query)

        with self.engine.begin() as conn:
            conn.execute(query, params or {})
