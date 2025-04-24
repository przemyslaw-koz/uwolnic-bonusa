import json
import os
from logging import debug

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.util import ScopedRegistry

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)
CORS(app)


class Sign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)


@app.route("/data", methods=["GET"])
def get_data():
    data = Sign.query.all()
    return jsonify(
        [
            {
                "name": s.name,
                "nickname": s.nickname,
                "city": s.city,
                "message": s.message,
            }
            for s in data
        ]
    )


@app.route("/sign", methods=["POST"])
def sign():
    data = request.get_json()
    new_sign = Sign()
    new_sign.name = data["name"]
    new_sign.nickname = data["nickname"]
    new_sign.city = data["city"]
    new_sign.message = data["message"]

    db.session.add(new_sign)
    db.session.commit()
    return jsonify({"message": "New sign added"}), 200


@app.route("/")
def root():
    return "Uwolnić BONUSA 🚀"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
