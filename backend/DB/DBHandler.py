from typing import Dict
import json
import datetime
import oracledb
import pprint

from DBConnector import DBConnector


class DBHandler:
    def __init__(self, wallet_credentials: Dict):
        self.db_connector = DBConnector(wallet_credentials)
        self.connection = self.db_connector.get_connection()

    def get_food_list(self) -> str:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT food_id, name, calories_per_100g, proteins_per_100g, fats_per_100g, carbohydrates_per_100g, serving, water FROM food"
            )
            rows = cursor.fetchall()
            return json.dumps(
                [
                    {
                        "food_id": row[0],
                        "name": row[1],
                        "calories_per_100": row[2],
                        # "proteins_per_100": row[3],
                        # "fats_per_100": row[4],
                        # "carbohydrates_per_100": row[5],
                        "serving": row[6],
                        # "water_per_100": row[7],
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
            meal_id = self._find_meal(date_time, meal_type)
            if not meal_id:
                meal_id = self._insert_empty_meal(meal_type)
                self._insert_empty_meal_entry(meal_id, user_id, date_time)

            self._insert_meal_food(meal_id, food_id, quantity)
            self.commit()
        except oracledb.DatabaseError as e:
            print("Error in add_meal_food")
            print(e)

    def _find_meal(self, date_time: str, meal_type: int) -> int:
        query = """
        SELECT meal_meal_id
        FROM meal_entry
        JOIN meal ON meal_entry.meal_meal_id = meal.meal_id
        WHERE TRUNC(meal_entry.date_time) = TRUNC(TO_DATE(:date_time, 'DD-MM-YYYY'))  AND meal.meal_type_meal_type_id = :meal_type
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"date_time": date_time, "meal_type": meal_type})
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

    def _insert_empty_meal(self, meal_type: int) -> int:
        query = """
        INSERT INTO meal (water_consumption, calories, proteins, fats, carbohydrates, meal_type_meal_type_id, meal_id)
        VALUES (0, 0.1, 0, 0, 0, :meal_type, :meal_id)"""
        meal_id = self._find_next_meal_id()
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"meal_type": meal_type, "meal_id": meal_id})
        return meal_id

    def _find_next_meal_id(self) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT MAX(meal_id) FROM meal")
            result = cursor.fetchone()
            if result[0] is None:
                return 1
            else:
                return result[0] + 1

    def _insert_empty_meal_entry(self, meal_id: int, user_id: int, date_time: str):
        query = """
        INSERT INTO meal_entry (meal_entry_id, user_user_id, meal_meal_id, date_time)
        VALUES (:meal_entry_id, :user_id, :meal_id, TO_DATE(:date_time, 'DD-MM-YYYY'))"""
        meal_entry_id = self._find_next_meal_entry_id()
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

    def _find_next_meal_entry_id(self) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT MAX(meal_entry_id) FROM meal_entry")
            result = cursor.fetchone()
            if result[0] is None:
                return 1
            else:
                return result[0] + 1

    def get_day_history(self, day_dict) -> str:
        # DO POprawy gdy nie znajdzie#################
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
        WHERE TRUNC(me.date_time) = TRUNC(TO_DATE(:query_date, 'DD-MM-YYYY')) AND me.user_user_id = :user_id
        """
        meal_info = []
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"query_date": date, "user_id": user_id})
            meals = cursor.fetchall()

            for meal in meals:
                meal_type_name, calories, proteins, fats, carbs, meal_id = meal
                meal_info.append(
                    {
                        "meal_type": meal_type_name,
                        "kcal": calories,
                        "proteins": proteins,
                        "fats": fats,
                        "carbs": carbs,
                        "foods": self._get_foods_for_meal(meal_id),
                    }
                )

        return json.dumps(meal_info, indent=4)

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

    def add_body_measurement_entry(self, entry_dict: Dict):
        user_id = entry_dict["user_id"]
        date = entry_dict["date"]
        weight = entry_dict["weight"]

        query = """
        INSERT INTO body_measurement_entry (body_measurement_entry_id, date_time, weight, user_user_id)
        VALUES (:bm_id, TO_DATE(:date_time, 'DD-MM-YYYY-HH24'), :weight, :user_id)
        """
        bm_id = self._get_body_measurement_id()
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

    def _get_body_measurement_id(self) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT MAX(body_measurement_entry_id) FROM body_measurement_entry"
            )
            result = cursor.fetchone()
            if result[0] is None:
                return 1
            else:
                return result[0] + 1

    def add_activity_entry(self, activity_dict: Dict):
        user_id = activity_dict["user_id"]
        date = activity_dict["date"]
        activity_id = activity_dict["activity_id"]
        duration = activity_dict["duration"]
        calories_burned = activity_dict["calories_burned"]
        query = """
        INSERT INTO activity_entry (activity_entry_id, date_time, duration, calories_burned, user_user_id, activity_activity_id)
        VALUES (:activity_entry_id, TO_DATE(:date_time, 'DD-MM-YYYY-HH24-MI'), :duration, :calories_burned, :user_id, :activity_id)"""
        activity_entry_id = self._get_activity_entry_id()
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

    def _get_activity_entry_id(self) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT MAX(activity_entry_id) FROM activity_entry")
            result = cursor.fetchone()
            if result[0] is None:
                return 1
            else:
                return result[0] + 1

    def get_activity_history(self, user_id: int) -> str:
        query = """
        SELECT TO_CHAR(ae.date_time, 'DD-MM-YYYY-HH24-MI') AS date_time, a.name AS activity_name, ae.duration, ae.calories_burned
        FROM activity_entry ae
        JOIN activity a ON ae.activity_activity_id = a.activity_id
        WHERE ae.user_user_id = :user_id
        ORDER BY ae.date_time
        """
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
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT activity_id, "NAME", calories_per_hour FROM activity"""
            )
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

    def get_goal_types_list(self) -> str:
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT name FROM goal_type""")
            rows = cursor.fetchall()
            return json.dumps(
                [row[0] for row in rows],
                indent=4,
            )

    def get_user_goal(self, goal_dict: Dict) -> str:
        user_id = goal_dict["user_id"]
        date = goal_dict["date"]
        query = """
        SELECT gt.name, target_weight, TO_CHAR(start_date, 'DD-MM-YYYY'), TO_CHAR(end_date, 'DD-MM-YYYY')
        FROM goal g
        JOIN goal_type gt ON g.goal_type_goal_type_id = gt.goal_type_id
        WHERE user_user_id = :user_id
            AND start_date <= TO_DATE(:date_time, 'DD-MM-YYYY')
            AND end_date >= TO_DATE(:date_time, 'DD-MM-YYYY')
        ORDER BY end_date ASC
        FETCH FIRST 1 ROW ONLY
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, {"user_id": user_id, "date_time": date})
            result = cursor.fetchone()
            if result:
                return json.dumps(
                    {
                        "goal_type": result[0],
                        "target_weight": result[1],
                        "start_date": result[2],
                        "end_date": result[3],
                    },
                    indent=4,
                )
            return json.dumps(
                {
                    "goal_type": "No goal set",
                    "target_weight": "",
                    "start_date": "",
                    "end_date": "",
                },
                indent=4,
            )

    def set_user_goal(self, goal_dict: Dict):
        user_id = goal_dict["user_id"]
        goal_type = goal_dict["goal_type"]
        target_weight = goal_dict["target_weight"]
        start_date = goal_dict["start_date"]
        end_date = goal_dict["end_date"]

        query = """
        INSERT INTO goal (goal_id, target_weight, start_date, end_date, user_user_id, goal_type_goal_type_id)
        VALUES (:goal_id, :target_weight, TO_DATE(:start_date, 'DD-MM-YYYY'), TO_DATE(:end_date, 'DD-MM-YYYY'), :user_id, :goal_type)
        """
        goal_id = self._get_goal_id()
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
                {
                    "goal_id": goal_id,
                    "target_weight": target_weight,
                    "start_date": start_date,
                    "end_date": end_date,
                    "user_id": user_id,
                    "goal_type": goal_type,
                },
            )
        self.commit()

    def _get_goal_id(self) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT MAX(goal_id) FROM goal")
            result = cursor.fetchone()
            if result[0] is None:
                return 1
            else:
                return result[0] + 1

    def close(self):
        self.db_connector.close()

    def commit(self):
        self.connection.commit()


def main():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = DBHandler(wallet_credentials=wallet_credentials)

    with open("backend/DB/examples/foods.json", "w", encoding="utf-8") as f:
        f.write(db.get_food_list())
    # # db.add_meal_food(
    # #     {
    # #         "date_time": "19-04-2024",
    # #         "food_id": 9002,
    # #         "quantity": 100,
    # #         "meal_type": 92,
    # #         "user_id": 9001,
    # #     }
    # # )

    # with open("backend/DB/examples/history.json", "w", encoding="utf-8") as f:
    #     f.write(db.get_day_history({"date": "19-04-2024", "user_id": 9001}))

    # db.add_body_measurement_entry({"user_id": 1, "date": "19-04-2024-14", "weight": 70})

    # with open("backend/DB/examples/body_measurement_history.json", "w", encoding="utf-8") as f:
    #     f.write(db.get_body_measurement_history(1))

    # db.add_activity_entry(
    #     {
    #         "user_id": 1,
    #         "date": "19-04-2024-16-00",
    #         "activity_id": 101,
    #         "duration": 60,
    #         "calories_burned": 200,
    #     }
    # )

    # with open("backend/DB/examples/activity_history.json", "w", encoding="utf-8") as f:
    #     f.write(db.get_activity_history(1))

    # # with open("backend/DB/examples/activity_list.json", "w", encoding="utf-8") as f:
    # #     f.write(db.get_activity_list())

    # # with open("backend/DB/examples/goal_type_list.json", "w", encoding="utf-8") as f:
    # #     f.write(db.get_goal_types_list())

    with open("backend/DB/examples/goal.json", "w", encoding="utf-8") as f:
        f.write(db.get_user_goal({"user_id": 1, "date": "24-05-2024"}))

    db.set_user_goal(
        {
            "user_id": 1,
            "goal_type": 1,
            "target_weight": 60,
            "start_date": "24-04-2024",
            "end_date": "24-09-2024",
        }
    )


if __name__ == "__main__":
    main()
