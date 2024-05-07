from typing import Dict
import json
import oracledb

from DBHandler import DBHandler


class MealHandler(DBHandler):
    def __init__(self, wallet_credentials: Dict):
        super().__init__(wallet_credentials)

    def get_food_list(self) -> str:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT food_id,
                    name,
                    calories_per_100g,
                    serving
                FROM food"""
            )
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

        try:
            meal_id = self._find_meal(date_time, meal_type, user_id)
            if not meal_id:
                meal_id = self._insert_empty_meal(meal_type)
                self._insert_empty_meal_entry(meal_id, user_id, date_time)

            self._insert_meal_food(meal_id, food_id, quantity)
            self.commit()
        except oracledb.DatabaseError as e:
            self.logger.error("Error in add_meal_food: %s", e)

    def _find_meal(self, date_time: str, meal_type: int, user_id: int) -> int:
        query = """
        SELECT meal_meal_id
        FROM meal_entry
        JOIN meal ON meal_entry.meal_meal_id = meal.meal_id
        JOIN meal_type ON meal.meal_type_meal_type_id = meal_type.meal_type_id
        WHERE TRUNC(meal_entry.date_time) = TRUNC(TO_DATE(:date_time, 'DD-MM-YYYY'))
            AND meal_type.name = :meal_type
            AND meal_entry.user_user_id = :user_id
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                {"date_time": date_time, "meal_type": meal_type, "user_id": user_id},
            )
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

    def _insert_empty_meal(self, meal_type: int) -> int:
        query = """
        INSERT INTO meal (water_consumption, calories, proteins,
        fats, carbohydrates, meal_type_meal_type_id, meal_id)
        VALUES (0, 0.1, 0, 0, 0, :meal_type, :meal_id)"""
        meal_id = self._find_next_id("meal")
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"meal_type": meal_type, "meal_id": meal_id})
        return meal_id

    def _insert_empty_meal_entry(self, meal_id: int, user_id: int, date_time: str):
        query = """
        INSERT INTO meal_entry (meal_entry_id, user_user_id, meal_meal_id, date_time)
        VALUES (:meal_entry_id, :user_id, :meal_id, TO_DATE(:date_time, 'DD-MM-YYYY'))"""
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
        query = """
        INSERT INTO meal_food (meal_meal_id, food_food_id, quantity)
        VALUES (:meal_id, :food_id, :quantity)"""
        with self.connection.cursor() as cursor:
            cursor.execute(
                query, {"meal_id": meal_id, "food_id": food_id, "quantity": quantity}
            )

    def get_day_history(self, day_dict) -> str:
        date = day_dict["date"]
        user_id = day_dict["user_id"]
        query = """
        SELECT mt.name AS meal_type_name,
            m.calories AS total_calories,
            m.proteins AS total_proteins,
            m.fats AS total_fats,
            m.carbohydrates AS total_carbs,
            m.meal_id
        FROM meal_entry me
        INNER JOIN meal m ON me.meal_meal_id = m.meal_id
        INNER JOIN meal_type mt ON m.meal_type_meal_type_id = mt.meal_type_id
        WHERE TRUNC(me.date_time) = TRUNC(TO_DATE(:query_date, 'DD-MM-YYYY'))
            AND me.user_user_id = :user_id
        """

        default_meal_info = {
            "Breakfast": {"kcal": 0, "proteins": 0, "fats": 0, "carbs": 0, "foods": []},
            "Second breakfast": {
                "kcal": 0,
                "proteins": 0,
                "fats": 0,
                "carbs": 0,
                "foods": [],
            },
            "Lunch": {"kcal": 0, "proteins": 0, "fats": 0, "carbs": 0, "foods": []},
            "Afternoon snack": {
                "kcal": 0,
                "proteins": 0,
                "fats": 0,
                "carbs": 0,
                "foods": [],
            },
            "Dinner": {"kcal": 0, "proteins": 0, "fats": 0, "carbs": 0, "foods": []},
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
        query = """
        SELECT f.name,
            f.calories_per_100g,
            f.proteins_per_100g,
            f.fats_per_100g,
            f.carbohydrates_per_100g,
            f.water,
            mf.quantity
        FROM meal_food mf
        INNER JOIN food f ON mf.food_food_id = f.food_id
        WHERE mf.meal_meal_id = :meal_id
        """
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

    def delete_food_from_meal(self, meal_data: Dict) -> bool:
        date_time = meal_data["date_time"]
        food_name = meal_data["food_name"]
        meal_type = meal_data["meal_type"]
        user_id = meal_data["user_id"]

        meal_id = self._find_meal(date_time, meal_type, user_id)
        food_id = self._find_food_id(food_name)
        if meal_id and food_id:
            query = """
            DELETE FROM meal_food
            WHERE meal_meal_id = :meal_id AND food_food_id = :food_id
            """
            with self.connection.cursor() as cursor:
                cursor.execute(query, {"meal_id": meal_id, "food_id": food_id})
            self.commit()
            return True
        return False

    def _find_food_id(self, food_name: str) -> int:
        query = """
        SELECT food_id
        FROM food
        WHERE name = :food_name
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"food_name": food_name})
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None


def main():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = MealHandler(wallet_credentials=wallet_credentials)

    with open("backend/DB/examples/foods.json", "w", encoding="utf-8") as f:
        f.write(db.get_food_list())
    db.add_meal_food(
        {
            "date_time": "19-04-2024",
            "food_id": 2,
            "quantity": 137,
            "meal_type": "Breakfast",
            "user_id": 1,
        }
    )

    # with open("backend/DB/examples/history.json", "w", encoding="utf-8") as f:
    #     f.write(db.get_day_history({"date": "19-04-2024", "user_id": 1}))

    # db.delete_food_from_meal(
    #     {
    #         "date_time": "01-04-2024",
    #         "food_name": "Oats",
    #         "meal_type": 1,
    #         "user_id": 1,
    #     }
    # )


if __name__ == "__main__":
    main()
