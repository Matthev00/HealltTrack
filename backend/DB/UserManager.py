import oracledb
import json
import bcrypt
from typing import Dict
from pathlib import Path

from DBHandler import DBHandler


class UserManager(DBHandler):
    def __init__(self, wallet_credentials: Dict):
        super().__init__(wallet_credentials)

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

        query = self._get_query("register_user")
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    query,
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

    def check_password(self, stored_pass: str, provided_pass: str) -> bool:
        return bcrypt.checkpw(provided_pass.encode(), stored_pass)

    def login_user(self, login_dict: Dict) -> Dict:
        email = login_dict["email"]
        password = login_dict["password"]
        query = self._get_query("login_user")
        with self.connection.cursor() as cursor:
            cursor.execute(
                query,
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
        query = self._get_query("get_user_data")

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


def main():
    folder_name = Path(__file__).parent
    with open(folder_name / "wallet_credentials.json") as f:
        wallet_credentials = json.load(f)

    user_manager = UserManager(wallet_credentials)

    if user_manager.register_user(
        {
            "name": "John",
            "surname": "Doe",
            "email": "xyz2@gmail.com",
            "password": "secret",
            "date_of_birth": "01-01-1999",
            "gender": "M",
            "height": 180,
        }
    ):
        print("User registered successfully!")
    else:
        print("Failed to register user.")

    login = user_manager.login_user(
        {"email": "xyz2@gmail.com", "password": "secret"}
    )  # f8

    examples = folder_name / "examples"
    if login:
        with open(examples / "login_data.json", "w", encoding="utf-8") as f:
            f.write(login)
    else:
        print("Failed to log in.")


if __name__ == "__main__":
    main()
