from flask import Flask, jsonify, request
from flask_cors import CORS
from DB.DBHandler import DBHandler
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/popup_food', methods=['GET'])
def return_home():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = DBHandler(wallet_credentials=wallet_credentials)
    food_list = db.get_food_list()
    return jsonify(food_list)  # Convert the food_list to JSON format


@app.route('/popup_food/<date>', methods=['GET'])
def display_data_in_specific_day(date):
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = DBHandler(wallet_credentials=wallet_credentials)
    date_data = {'date': date, 'user_id': 1}
    day_history = db.get_day_history(date_data)
    return jsonify(day_history)


@app.route('/popup_food_out', methods=['POST'])
def add_choosen_food():
    if request.method == 'POST':
        request_data = request.json

        # TODO: Send the data to the database

        return jsonify({"message": "Data has been sent"}), 200
    else:
        return jsonify({"error": "Unfortunately something gone wrong"}), 405


if __name__ == "__main__":
    app.run(debug=True, port=5000)
