from flask import Flask, jsonify
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
