from typing import Dict
import json
import oracledb
from pathlib import Path

from DBHandler import DBHandler


class MealHandler(DBHandler):
    def __init__(self, wallet_credentials: Dict):
        super().__init__(wallet_credentials)

    def get_food_list(self) -> str:
        query = self._get_query("get_food_list")
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return json.dumps(
                [
                    {
                        "food_id": row[0],
                        "name": row[1],
                        "calories_per_100": row[2],
                        "serving": row[3],
                    }
                    for row in rows
                ],
                indent=4,
            )

    def add_meal_food(self, meal_data: Dict) -> str:
        date_time = meal_data["date_time"]  # should be in format 'DD-MM-YYYY'
        food_id = meal_data["food_id"]
        quantity = meal_data["quantity"]
        meal_type = meal_data["meal_type"]
        user_id = meal_data["user_id"]
        meal_type_id = self._get_meal_type_id(meal_type)

        try:
            meal_id = self._find_meal(date_time, meal_type, user_id)
            if not meal_id:
                meal_id = self._insert_empty_meal(meal_type_id)
                self._insert_empty_meal_entry(meal_id, user_id, date_time)

            self._insert_meal_food(meal_id, food_id, quantity)
            self.commit()
        except oracledb.DatabaseError as e:
            self.logger.error("Error in add_meal_food: %s", e)

    def _get_meal_type_id(self, meal_type: str) -> int:
        query = self._get_query("get_meal_type_id")
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"meal_type_name": meal_type})
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

    def _find_meal(self, date_time: str, meal_type: int, user_id: int) -> int:
        query = self._get_query("find_meal")
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                {
                    "date_time": date_time,
                    "meal_type": meal_type,
                    "user_id": user_id,
                },  #
            )
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

    def _insert_empty_meal(self, meal_type: int) -> int:
        query = self._get_query("insert_empty_meal")
        meal_id = self._find_next_id("meal")
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"meal_type": meal_type, "meal_id": meal_id})
        return meal_id

    def _insert_empty_meal_entry(
        self, meal_id: int, user_id: int, date_time: str
    ) -> None:
        query = self._get_query("insert_empty_meal_entry")
        meal_entry_id = self._find_next_id("meal_entry")
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                {
                    "meal_entry_id": meal_entry_id,
                    "user_id": user_id,
                    "meal_id": meal_id,
                    "date_time": date_time,
                },
            )

    def _insert_meal_food(self, meal_id: int, food_id: int, quantity: int):
        query = self._get_query("insert_meal_food")
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                {
                    "meal_id": meal_id,
                    "food_id": food_id,
                    "quantity": quantity,
                },  #
            )

    def get_day_history(self, day_dict) -> str:
        date = day_dict["date"]
        user_id = day_dict["user_id"]
        query = self._get_query("get_day_history")

        default_meal_info = {
            "Breakfast": {
                "kcal": 0,
                "proteins": 0,
                "fats": 0,
                "carbs": 0,
                "foods": [],
            },
            "Lunch": {
                "kcal": 0,
                "proteins": 0,
                "fats": 0,
                "carbs": 0,
                "foods": [],
            },
            "Dinner": {
                "kcal": 0,
                "proteins": 0,
                "fats": 0,
                "carbs": 0,
                "foods": [],
            },
            "Snack": {
                "kcal": 0,
                "proteins": 0,
                "fats": 0,
                "carbs": 0,
                "foods": [],
            },
            "Supper": {
                "kcal": 0,
                "proteins": 0,
                "fats": 0,
                "carbs": 0,
                "foods": [],
            },
        }

        with self.connection.cursor() as cursor:
            cursor.execute(query, {"query_date": date, "user_id": user_id})
            meals = cursor.fetchall()

            for meal in meals:
                meal_type_name, calories, proteins, fats, carbs, meal_id = meal
                default_meal_info[meal_type_name] = {
                    "kcal": calories,
                    "proteins": proteins,
                    "fats": fats,
                    "carbs": carbs,
                    "foods": self._get_foods_for_meal(meal_id),
                }

        return json.dumps(default_meal_info, indent=4)

    def _get_foods_for_meal(self, meal_id: int) -> list:
        query = self._get_query("get_foods_for_meal")
        foods = []
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"meal_id": meal_id})
            rows = cursor.fetchall()
            for row in rows:
                name, calories, proteins, fats, carbs, water, quantity = row
                foods.append(
                    {
                        "name": name,
                        "calories_per_100g": calories,
                        "proteins_per_100g": proteins,
                        "fats_per_100g": fats,
                        "carbohydrates_per_100g": carbs,
                        "water_per_100g": water,
                        "quantity": quantity,
                    }
                )
        return foods

    def get_day_macros(self, day_dict) -> str:
        date = day_dict["date"]
        user_id = day_dict["user_id"]
        query = self._get_query("get_day_macros")

        with self.connection.cursor() as cursor:
            cursor.execute(query, {"query_date": date, "user_id": user_id})
            result = cursor.fetchone()
            if result:
                macros = {
                    "kcal": result[0],
                    "proteins": result[1],
                    "fats": result[2],
                    "carbs": result[3],
                    "water": result[4],
                }
            else:
                macros = {
                    "kcal": 0,
                    "proteins": 0,
                    "fats": 0,
                    "carbs": 0,
                    "water": 0,
                }
        return json.dumps(macros, indent=4)

    def delete_food_from_meal(self, meal_data: Dict) -> bool:
        date_time = meal_data["date_time"]
        food_name = meal_data["food_name"]
        meal_type = meal_data["meal_type"]
        user_id = meal_data["user_id"]

        meal_id = self._find_meal(date_time, meal_type, user_id)
        food_id = self._find_food_id(food_name)
        if meal_id and food_id:
            query = self._get_query("delete_food_from_meal")
            with self.connection.cursor() as cursor:
                cursor.execute(query, {"meal_id": meal_id, "food_id": food_id})
            self.commit()
            return True
        return False

    def _find_food_id(self, food_name: str) -> int:
        query = self._get_query("find_food_id")
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"food_name": food_name})
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None


def main():
    folder_name = Path(__file__).parent
    with open(folder_name / "wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = MealHandler(wallet_credentials=wallet_credentials)

    examples = folder_name / "examples"
    # with open(examples / "foods.json", "w", encoding="utf-8") as f:
    #     f.write(db.get_food_list())
    # db.add_meal_food(
    #     {
    #         "date_time": "19-04-2024",
    #         "food_id": 2,
    #         "quantity": 137,
    #         "meal_type": "Breakfast",
    #         "user_id": 1,
    #     }
    # )

    # with open(examples / "history.json", "w", encoding="utf-8") as f:
    #     f.write(db.get_day_history({"date": "19-04-2024", "user_id": 1}))

    # db.delete_food_from_meal(
    #     {
    #         "date_time": "01-04-2024",
    #         "food_name": "Oats",
    #         "meal_type": "Breakfast",
    #         "user_id": 1,
    #     }
    # )

    with open(examples / "day_macros.json", "w", encoding="utf-8") as f:
        f.write(db.get_day_macros({"date": "30-04-2024", "user_id": 1}))


if __name__ == "__main__":
    main()
