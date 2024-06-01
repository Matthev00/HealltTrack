from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import json
import datetime

sys.path.append("backend/DB")
from MealHandler import MealHandler  # noqa 5501
from ActivityHandler import ActivityHandler  # noqa 5501
from GoalHandler import GoalHandler  # noqa 5501
from MeasurementHandler import MeasurementHandler  # noqa 5501

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


def get_current_time() -> str:
    return datetime.datetime.now().strftime("%H-%M-%S")


def connect_to_db_meal():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = MealHandler(wallet_credentials=wallet_credentials)
    return db


def connect_to_db_activity():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = ActivityHandler(wallet_credentials=wallet_credentials)
    return db


def connect_to_db_goal():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = GoalHandler(wallet_credentials=wallet_credentials)
    return db


def connect_to_db_measurement():
    with open("backend/DB/wallet_credentials.json") as f:
        wallet_credentials = json.load(f)
    db = MeasurementHandler(wallet_credentials=wallet_credentials)
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


@app.route('/macros/<user_id>/<date>', methods=['GET'])
def get_day_macros(user_id, date):
    db = connect_to_db_meal()
    date_data = {'date': date, 'user_id': user_id}
    day_macros = db.get_day_macros(date_data)
    return jsonify(day_macros)


@app.route('/popup_food_out', methods=['POST'])
def add_choosen_food():
    if request.method == 'POST':
        request_data = request.json
        db = connect_to_db_meal()
        request_data['user_id'] = 1

        db.add_meal_food(request_data)
        return jsonify({"message": "Data has been sent"}), 200
    else:
        return jsonify({"error": "Unfortunately something gone wrong"}), 405


@app.route('/delete_food', methods=['POST'])
def delete_meal_food():
    if request.method == 'POST':
        request_data = request.json
        request_data['user_id'] = 1
        db = connect_to_db_meal()
        db.delete_food_from_meal(request_data)
        return jsonify({"message": "Data has been sent"}), 200
    else:
        return jsonify({"error": "Unfortunately something gone wrong"}), 405


@app.route('/activity_out', methods=['POST'])
def add_performed_activity():
    if request.method == 'POST':
        request_data = request.json
        db = connect_to_db_activity()
        db.add_activity_entry(request_data)
        return jsonify({"message": "Data has been sent"}), 200
    else:
        return jsonify({"error": "Unfortunately something gone wrong"}), 405


@app.route('/activity/<id>', methods=['GET'])
def get_activity_history(id):
    db = connect_to_db_activity()
    activity_history = db.get_activity_history(id)
    return jsonify(activity_history)


@app.route('/activity/<id>/<date>', methods=['GET'])
def get_activity_day_history(id, date):
    db = connect_to_db_activity()
    print(id)
    print(date)
    activity_history = db.get_activity_day_history(id, date)
    return jsonify(activity_history)


@app.route('/activity_list', methods=['GET'])
def get_activity_list():
    db = connect_to_db_activity()
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


@app.route('/user_goal/get', methods=['GET'])
def get_user_goal():
    db = connect_to_db_goal()
    date = request.json['date']
    user_goal_data = {'user_id': 1, 'date': date}
    user_goals = db.get_user_goal(user_goal_data)
    return jsonify(user_goals)


@app.route('/user_goal/add', methods=['POST'])
def add_user_goal():
    db = connect_to_db_goal()
    user_goal_data = {'user_id': 1,
                      'goal_type': 'lose_weight',
                      'target_weight': request.json['target_weight'],
                      'start_date': request.json['start_date'],
                      'end_date': request.json['end_date']}
    user_goal = db.set_user_goal(user_goal_data)
    return jsonify(user_goal)


@app.route('/body_measurement/history/<id>', methods=['GET'])
def get_body_measurement_history(id):
    db = connect_to_db_measurement()
    user_body_measurement = db.get_body_measurement_history(id)
    return jsonify(user_body_measurement)


@app.route('/body_measurement/add', methods=['POST'])
def add_body_measurement_specific_day():
    if request.method == 'POST':
        db = connect_to_db_measurement()
        date = request.json['date']
        time = get_current_time()
        date += "-" + time
        weight = request.json['weight']
        body_measurement_data = {'user_id': 1, 'date': date, 'weight': weight}
        db.add_body_measurement_entry(body_measurement_data)
        return jsonify({"message": "Data has been sent"}), 200
    else:
        return jsonify({"error": "Unfortunately something gone wrong"}), 405


@app.route('/body_measurement/get/<date>', methods=['GET'])
def get_body_measurement_specific_day(date):
    db = connect_to_db_measurement()
    body_measurement_data = {'user_id': 1, 'date': date}
    user_body_measurement = db.get_body_measurement_day(
        body_measurement_data)
    return user_body_measurement


if __name__ == "__main__":
    db = connect_to_db_measurement()
    app.run(debug=True, port=5000)
