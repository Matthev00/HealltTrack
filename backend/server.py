from flask import Flask, jsonify, request
from flask_cors import CORS
from DB.DBHandler import DBHandler
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def connect_to_db():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = DBHandler(wallet_credentials=wallet_credentials)
    return db


@app.route('/popup_food', methods=['GET'])
def return_home():
    db = connect_to_db()
    food_list = db.get_food_list()
    return jsonify(food_list)  # Convert the food_list to JSON format


@app.route('/popup_food/<date>', methods=['GET'])
def display_data_in_specific_day(date):
    db = connect_to_db()
    date_data = {'date': date, 'user_id': 1}
    day_history = db.get_day_history(date_data)
    return jsonify(day_history)


@app.route('/popup_food_out', methods=['POST'])
def add_choosen_food():
    if request.method == 'POST':
        request_data = request.json
        db = connect_to_db()
        request_data['user_id'] = 1
        request_data['meal_type'] = "Breakfast"
        db.add_meal_food(request_data)
        return jsonify({"message": "Data has been sent"}), 200
    else:
        return jsonify({"error": "Unfortunately something gone wrong"}), 405


@app.route('/activity/<id>', methods=['GET'])
def get_activity_hisotry(id):
    db = connect_to_db()
    activity_history = db.get_activity_history(id)
    return jsonify(activity_history)


@app.route('/activity_list', methods=['GET'])
def get_activity_list():
    db = connect_to_db()
    activity_list = db.get_activity_list()
    return jsonify(activity_list)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
