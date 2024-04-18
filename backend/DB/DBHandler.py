from typing import Dict
import json
import datetime

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

    def add_meal_food(self, dict: Dict) -> str:
        date_time = self.convert_date_format(dict["date_time"])
        food_id = dict["food_id"]
        quantity = dict["quantity"]
        meal_type = dict["meal_type"]
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT meal_entry_id, date_time FROM meal_entry WHERE date_time = :date_time",
                date_time=date_time,
            )
            


    def convert_date_format(date_str: str) -> str:
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        return date_obj.strftime('%Y-%m-%d')

    def close(self):
        self.db_connector.close()
