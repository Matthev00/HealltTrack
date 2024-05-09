from typing import Dict
import json
import oracledb
from pathlib import Path

from DBHandler import DBHandler


class ActivityHandler(DBHandler):
    def __init__(self, wallet_credentials: Dict):
        super().__init__(wallet_credentials)

    def add_activity_entry(self, activity_dict: Dict):
        user_id = activity_dict["user_id"]
        date = activity_dict["date"]
        activity_id = activity_dict["activity_id"]
        duration = activity_dict["duration"]
        calories_burned = activity_dict["calories_burned"]
        query = self._get_query("add_activity_entry")
        activity_entry_id = self._find_next_id("activity_entry")
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    {
                        "activity_entry_id": activity_entry_id,
                        "date_time": date,
                        "duration": duration,
                        "calories_burned": calories_burned,
                        "user_id": user_id,
                        "activity_id": activity_id,
                    },
                )
            self.commit()
        except oracledb.DatabaseError as e:
            self.logger.error("Error in add_activity_entry: %s", e)

    def get_activity_history(self, user_id: int) -> str:
        query = self._get_query("get_activity_history")
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"user_id": user_id})
            rows = cursor.fetchall()
            return json.dumps(
                [
                    {
                        "date_time": row[0],
                        "activity_name": row[1],
                        "duration": row[2],
                        "calories_burned": row[3],
                    }
                    for row in rows
                ],
                indent=4,
            )

    def get_activity_list(self) -> str:
        query = self._get_query("get_activity_list")
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return json.dumps(
                [
                    {
                        "activity_id": row[0],
                        "name": row[1],
                        "calories_burned_per_minute": row[2],
                    }
                    for row in rows
                ],
                indent=4,
            )


def main():
    folder_name = Path(__file__).parent
    with open(folder_name / "wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = ActivityHandler(wallet_credentials=wallet_credentials)

    # db.add_activity_entry(
    #     {
    #         "user_id": 1,
    #         "date": "19-04-2024-16-00",
    #         "activity_id": 101,
    #         "duration": 60,
    #         "calories_burned": 200,
    #     }
    # )

    examples = folder_name / "examples"
    with open(examples / "activity_history.json", "w", encoding="utf-8") as f:
        f.write(db.get_activity_history(1))

    with open(examples / "activity_list.json", "w", encoding="utf-8") as f:
        f.write(db.get_activity_list())


if __name__ == "__main__":
    main()
