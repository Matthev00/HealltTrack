from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import json

sys.path.append("backend/DB")
from MealHandler import MealHandler
from ActivityHandler import ActivityHandler
from GoalHandler import GoalHandler
from MeasurementHandler import MeasurementHandler

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def connect_to_db_meal():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = MealHandler(wallet_credentials=wallet_credentials)
    return db


def connect_to_db_activity():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = MealHandler(wallet_credentials=wallet_credentials)
    return db


def connect_to_db_goal():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = MealHandler(wallet_credentials=wallet_credentials)
    return db


def connect_to_db_measurement():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = MealHandler(wallet_credentials=wallet_credentials)
    return db


@app.route('/popup_food', methods=['GET'])
def return_home():
    db = connect_to_db_meal()
    food_list = db.get_food_list()
    return jsonify(food_list)  # Convert the food_list to JSON format


@app.route('/popup_food/<date>', methods=['GET'])
def display_data_in_specific_day(date):
    db = connect_to_db_meal()
    date_data = {'date': date, 'user_id': 1}
    day_history = db.get_day_history(date_data)
    return jsonify(day_history)


@app.route('/popup_food_out', methods=['POST'])
def add_choosen_food():
    if request.method == 'POST':
        request_data = request.json
        db = connect_to_db_meal()
        request_data['user_id'] = 1
        request_data['meal_type'] = "Breakfast"
        db.add_meal_food(request_data)
        return jsonify({"message": "Data has been sent"}), 200
    else:
        return jsonify({"error": "Unfortunately something gone wrong"}), 405


@app.route('/activity/<id>', methods=['GET'])
def get_activity_hisotry(id):
    db = connect_to_db_activity()
    activity_history = db.get_activity_history(id)
    return jsonify(activity_history)


@app.route('/activity_list', methods=['GET'])
def get_activity_list():
    db = connect_to_db_meal()
    activity_list = db.get_activity_list()
    return jsonify(activity_list)


@app.route('/goal_type_list', methods=['GET'])
def get_goal_type_list():
    db = connect_to_db_goal()
    goal_type_list = db.get_goal_types_list()
    return jsonify(goal_type_list)


@app.route('/user_goal/<id>/<date>', methods=['GET'])
def get_user_goals(id, date):
    db = connect_to_db_goal()
    user_goal_data = {'user_id': id, 'date': date}
    user_goals = db.get_user_goal(user_goal_data)
    return jsonify(user_goals)


@app.route('/body_measurement/<id>', methods=['GET'])
def get_body_measurement_history(id):
    db = connect_to_db_measurement()
    user_body_measurement = db.get_body_measurement_history(id)
    return jsonify(user_body_measurement)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
