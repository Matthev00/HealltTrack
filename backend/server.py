from flask import Flask
from DB.DBHandler import DBHandler
import json

app = Flask(__name__)


@app.route('/popup_food', methods=['GET'])
def return_home():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = DBHandler(wallet_credentials=wallet_credentials)
    food_list = db.get_food_list()
    return food_list


if __name__ == "__main__":
    app.run(debug=True, port=5000)
