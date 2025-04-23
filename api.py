import json
import os
from logging import debug

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://uwolnic-bonusa-petycja.onrender.com"])
DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_data(new_item):
    data = load_data()
    data.append(new_item)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/data", methods=["GET"])
def get_data():
    data = load_data()
    return jsonify(data)


@app.route("/sign", methods=["POST"])
def sign():
    new_sign = request.get_json()
    save_data(new_sign)
    return jsonify({"message": "New sign added"}), 200


@app.route("/")
def root():
    return "Uwolnić BONUSA 🚀"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
