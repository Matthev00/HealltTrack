from typing import Dict
import json
import oracledb
from pathlib import Path

from DBHandler import DBHandler


class MeasurementHandler(DBHandler):
    def __init__(self, wallet_credentials: Dict):
        super().__init__(wallet_credentials)

    def add_body_measurement_entry(self, entry_dict: Dict):
        user_id = entry_dict["user_id"]
        date = entry_dict["date"]
        weight = entry_dict["weight"]

        query = self._get_query("add_body_measurement_entry")
        bm_id = self._find_next_id("body_measurement_entry")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    {
                        "bm_id": bm_id,
                        "date_time": date,
                        "weight": weight,
                        "user_id": user_id,
                    },
                )
            self.commit()
        except oracledb.DatabaseError as e:
            self.logger.error("Error in add_body_measurement_entry: %s", e)

    def get_body_measurement_history(self, user_id: int) -> str:
        query = self._get_query("get_body_measurement_history")
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"user_id": user_id})
            rows = cursor.fetchall()
            return json.dumps(
                [{"date_time": row[0], "weight": row[1]} for row in rows],
                indent=4,
            )


def main():
    folder_name = Path(__file__).parent
    with open(folder_name / "wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = MeasurementHandler(wallet_credentials=wallet_credentials)

    db.add_body_measurement_entry(
        {"user_id": 1, "date": "19-04-2024-14", "weight": 70}
    )  #

    exemples = folder_name / "examples"
    with open(
        exemples / "body_measurement_history.json", "w", encoding="utf-8"
    ) as f:  #
        f.write(db.get_body_measurement_history(1))


if __name__ == "__main__":
    main()
