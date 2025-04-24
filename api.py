import json
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)


class Sign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)


def create_tables_and_seed():
    with app.app_context():
        db.create_all()
        if Sign.query.count() == 1:
            try:
                with open("data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        sign = Sign(
                            name=item["name"],
                            nickname=item["nickname"],
                            city=item["city"],
                            message=item["message"],
                        )
                        db.session.add(sign)
                    db.session.commit()
                print("Dane z data.json zostały załadowane do bazy danych.")
            except FileNotFoundError:
                print("Plik data.json nie został znaleziony.  Dodaję puste dane.")
                sample = Sign(
                    name="Piotr",
                    nickname="Bonus BGC",
                    city="Łazarski",
                    message="Uwolnijcie mnie natychmiast!",
                )
                db.session.add(sample)
                db.session.commit()


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
    create_tables_and_seed()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
