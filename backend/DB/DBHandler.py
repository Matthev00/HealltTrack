from typing import Dict
import logging
from pathlib import Path

from DBConnector import DBConnector


class DBHandler:
    def __init__(self, wallet_credentials: Dict):
        self.db_connector = DBConnector(wallet_credentials)
        self.connection = self.db_connector.get_connection()
        self.logger = logging.getLogger(__name__)
        self._queries_path = Path(__file__).parent / "queries"

    def _find_next_id(self, table_name: str) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT MAX({table_name}_id) FROM {table_name}")
            result = cursor.fetchone()
        return result[0] + 1 if result[0] else 1

    def _get_query(self, query_name: str) -> str:
        with open(self._queries_path / f"{query_name}.sql") as f:
            return f.read()

    def close(self):
        self.db_connector.close()

    def commit(self):
        self.connection.commit()
