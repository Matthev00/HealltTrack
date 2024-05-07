from typing import Dict
import json
import oracledb

from DBHandler import DBHandler


class GoalHandler(DBHandler):
    def __init__(self, wallet_credentials: Dict):
        super().__init__(wallet_credentials)

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
        goal_id = self._find_next_id("goal")
        try:
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
        except oracledb.DatabaseError as e:
            self.logger.error("Error in set_user_goal: %s", e)


def main():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = GoalHandler(wallet_credentials=wallet_credentials)

    with open("backend/DB/examples/goal_type_list.json", "w", encoding="utf-8") as f:
        f.write(db.get_goal_types_list())

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
