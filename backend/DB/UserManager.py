import oracledb
import json
import bcrypt
from typing import Dict

from DBConnector import DBConnector


class UserManager:
    def __init__(self, db_connector: DBConnector):
        self.db_connector = db_connector
        self.connection = self.db_connector.get_connection()

    def hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def register_user(self, user_dict: Dict) -> bool:
        name = user_dict["name"]
        surname = user_dict["surname"]
        email = user_dict["email"]
        password = user_dict["password"]
        date_of_birth = user_dict["date_of_birth"]
        gender = user_dict["gender"]
        height = user_dict["height"]
        password_hash = self.hash_password(password)
        user_id = self._find_user_next_id()
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    """INSERT INTO "User" (user_id, name, surname, email, password, date_of_birth, gender, height)
                    VALUES (:user_id, :name, :surname, :email, :password, TO_DATE(:date_of_birth, 'DD-MM-YYYY'), :gender, :height)""",
                    {
                        "user_id": user_id,
                        "name": name,
                        "surname": surname,
                        "email": email,
                        "password": password_hash,
                        "date_of_birth": date_of_birth,
                        "gender": gender,
                        "height": height,
                    },
                )
                self.commit()
            except oracledb.IntegrityError:
                print("Email already exists")
                return False
        return True

    def _find_user_next_id(self) -> int:
        with self.connection.cursor() as cursor:
            cursor.execute("""SELECT MAX(user_id) FROM "User" """)
            max_id = cursor.fetchone()
            return max_id[0] + 1 if max_id[0] else 1

    def check_password(self, stored_password: str, provided_password: str) -> bool:
        return bcrypt.checkpw(provided_password.encode(), stored_password)

    def login_user(self, login_dict: Dict) -> Dict:
        email = login_dict["email"]
        password = login_dict["password"]
        with self.connection.cursor() as cursor:
            cursor.execute(
                """SELECT password FROM "User" WHERE email = :email""",
                {"email": email},
            )
            stored_password = cursor.fetchone()
        if stored_password and self.check_password(
            bytes.fromhex(stored_password[0]), password
        ):
            return self.get_user_data(email)
        else:
            print("Login failed")
            return False

    def get_user_data(self, user_email: str) -> Dict:
        query = """SELECT user_id, name, surname, TO_CHAR(date_of_birth, 'DD-MM-YYYY'), gender , height
        FROM "User" WHERE email = :email"""

        with self.connection.cursor() as cursor:
            cursor.execute(query, {"email": user_email})
            result = cursor.fetchone()
            return json.dumps(
                {
                    "user_id": result[0],
                    "name": result[1],
                    "surname": result[2],
                    "date_of_birth": result[3],
                    "gender": result[4],
                    "height": result[5],
                },
                indent=4,
            )

    def commit(self):
        self.connection.commit()


def main():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)

    db_connector = DBConnector(wallet_credentials)
    user_manager = UserManager(db_connector)

    if user_manager.register_user(
        {
            "name": "John",
            "surname": "Doe",
            "email": "xyz@gmail.com",
            "password": "secret",
            "date_of_birth": "01-01-1999",
            "gender": "M",
            "height": 180,
        }
    ):
        print("User registered successfully!")
    else:
        print("Failed to register user.")

    login = user_manager.login_user({"email": "xyz@gmail.com", "password": "secret"})

    if login:
        with open("backend/DB/examples/login_data.json", "w", encoding="utf-8") as f:
            f.write(login)
    else:
        print("Failed to log in.")


if __name__ == "__main__":
    main()
