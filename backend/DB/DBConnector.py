import oracledb
from typing import Dict
import json


class DBConnector:
    _instance = None

    def __new__(cls, wallet_credentials: Dict):
        if cls._instance is None:
            cls._instance = super(DBConnector, cls).__new__(cls)
            cls._instance.read_credentials(wallet_credentials)
            cls._instance.connection = oracledb.connect(
                user=cls._instance.user,
                password=cls._instance.password,
                dsn=cls._instance.dsn,
                config_dir=cls._instance.config_dir,
                wallet_location=cls._instance.wallet_location,
                wallet_password=cls._instance.wallet_password,
            )
        return cls._instance

    def read_credentials(self, wallet_credentials: Dict):
        try:
            self.user = wallet_credentials["user"]
            self.password = wallet_credentials["password"]
            self.dsn = wallet_credentials["dsn"]
            self.config_dir = wallet_credentials["cdir"]
            self.wallet_location = wallet_credentials["wltloc"]
            self.wallet_password = wallet_credentials["wltpsw"]
        except KeyError as e:
            print(f"KeyError: {e} not found in wallet_credentials")
            raise

    def get_connection(self):
        return self.connection

    def __del__(self):
        self.connection.close()

    def close(self):
        self.connection.close()


def main():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)

    db_connector = DBConnector(wallet_credentials)
    connection = db_connector.get_connection()


if __name__ == "__main__":
    main()
