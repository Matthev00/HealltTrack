from typing import Dict
import json
import oracledb

from DBHandler import DBHandler


class MeasurementHandler(DBHandler):
    def __init__(self, wallet_credentials: Dict):
        super().__init__(wallet_credentials)

    def add_body_measurement_entry(self, entry_dict: Dict):
        user_id = entry_dict["user_id"]
        date = entry_dict["date"]
        weight = entry_dict["weight"]

        query = """
        INSERT INTO body_measurement_entry (body_measurement_entry_id, date_time, weight, user_user_id)
        VALUES (:bm_id, TO_DATE(:date_time, 'DD-MM-YYYY-HH24'), :weight, :user_id)
        """
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
        query = """
        SELECT TO_CHAR(bme.date_time, 'DD-MM-YYYY-HH24') AS date_time, bme.weight
        FROM body_measurement_entry bme
        WHERE bme.user_user_id = :user_id
        ORDER BY bme.date_time
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"user_id": user_id})
            rows = cursor.fetchall()
            return json.dumps(
                [{"date_time": row[0], "weight": row[1]} for row in rows],
                indent=4,
            )


def main():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = MeasurementHandler(wallet_credentials=wallet_credentials)

    # db.add_body_measurement_entry({"user_id": 1, "date": "19-04-2024-14", "weight": 70})

    with open("backend/DB/examples/body_measurement_history.json", "w", encoding="utf-8") as f:
        f.write(db.get_body_measurement_history(1))


if __name__ == "__main__":
    main()
