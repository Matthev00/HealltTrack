from typing import Dict
import logging

from DBConnector import DBConnector


class DBHandler:
    def __init__(self, wallet_credentials: Dict):
        self.db_connector = DBConnector(wallet_credentials)
        self.connection = self.db_connector.get_connection()
        self.logger = logging.getLogger(__name__)

    def _find_next_id(self, table_name: str) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT MAX({table_name}_id) FROM {table_name}")
            result = cursor.fetchone()
            if result[0] is None:
                return 1
            else:
                return result[0] + 1

    def close(self):
        self.db_connector.close()

    def commit(self):
        self.connection.commit()
