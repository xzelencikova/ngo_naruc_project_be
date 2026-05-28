import pandas as pd
from sqlalchemy.sql.elements import TextClause, Literal
from typing import Any

type RowList = list[dict[str, Any]]


class BaseRepository:
    def __init__(self, engine):
        self.engine = engine

    def _convert_to_dataframe(self, data: list[dict]) -> pd.DataFrame:
        return pd.DataFrame(data)

    def _convert_to_dict(self, df: pd.DataFrame) -> RowList:
        return df.to_dict(orient="records")

    def _load_data_to_db(
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
        with self.engine.begin() as conn:
            result = conn.execute(query, params or {})
            return result.mappings().all()

    def _commit(self, query: TextClause, params=None) -> int:
        """INSERT/UPDATE/DELETE queries that must be committed"""
        with self.engine.begin() as conn:
            result = conn.execute(query, params or {})
            return result.rowcount
