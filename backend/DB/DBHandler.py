from typing import Dict
import json
import datetime
import oracledb

from backend.DB.DBConnector import DBConnector


class DBHandler:
    def __init__(self, wallet_credentials: Dict):
        self.db_connector = DBConnector(wallet_credentials)
        self.connection = self.db_connector.get_connection()

    def get_food_list(self) -> str:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT food_id, name, calories_per_100, proteins_per_100, fats_per_100, carbohydrates_per_100, serving, water FROM food"
            )
            rows = cursor.fetchall()
            return json.dumps(
                [
                    {
                        "food_id": row[0],
                        "name": row[1],
                        "calories_per_100": row[2],
                        "proteins_per_100": row[3],
                        "fats_per_100": row[4],
                        "carbohydrates_per_100": row[5],
                        "serving": row[6],
                        "water_per_100": row[7],
                    }
                    for row in rows
                ]
            )

    def add_meal_food(self, meal_data: Dict) -> str:
        date_time = meal_data["date_time"]
        food_id = meal_data["food_id"]
        quantity = meal_data["quantity"]
        meal_type = meal_data["meal_type"]
        user_id = meal_data["user_id"]

        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT meal_entry_id FROM meal_entry JOIN meal ON meal_entry.meal_meal_id = meal.meal_id WHERE TRUNC(meal_entry.date_time) = TRUNC(TO_DATE(:date_time, 'DD-MM-YYYY')  AND meal.meal_type_meal_type_id = :meal_type",
                {"date_time": date_time, "meal_type": meal_type},
            )
            result = cursor.fetchone()

            if result:
                meal_id = result[0]
            else:
                cursor.execute("SELECT MAX(meal_id) FROM meal")
                result = cursor.fetchone()
                if result[0] is None:
                    meal_id = 1
                else:
                    meal_id = result[0] + 1
                cursor.execute(
                    "INSERT INTO meal (water_consumption, calories, proteins, fats, carbohydrates, meal_type_meal_type_id, meal_id) VALUES (0, 0, 0, 0, 0, :meal_type, :meal_id)",
                    {"meal_type": meal_type, "meal_id": meal_id},
                )
                cursor.execute("SELECT MAX(meal_entry_id) FROM meal_entry")
                result = cursor.fetchone()
                if result[0] is None:
                    meal_entry_id = 1
                else:
                    meal_entry_id = result[0] + 1
                cursor.execute(
                    "INSERT INTO meal_entry (meal_entry_id, user_user_id, meal_meal_id, date_time) VALUES (:meal_entry_id, :user_id, :meal_id, :date_time)",
                    {
                        "meal_entr_id": meal_entry_id,
                        "user_id": user_id,
                        "meal_id": meal_id,
                        "date_time": date_time,
                    },
                )

            cursor.execute(
                "INSERT INTO meal_food (meal_id, food_id, quantity) VALUES (:meal_id, :food_id, :quantity)",
                {"meal_id": meal_id, "food_id": food_id, "quantity": quantity},
            )

    def close(self):
        self.db_connector.close()
