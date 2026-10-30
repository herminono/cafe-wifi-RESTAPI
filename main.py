from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

with app.app_context():
    db.create_all()
    print("Database location:", db.engine.url.database)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    if not all_cafes:
        return jsonify(error="No cafes available."), 404
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all")
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(
            error="Sorry, we don't have a cafe at that location."
        ), 404

@app.route("/add", methods=["POST"])
def post_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=request.form.get("sockets", "").lower() == "true",
        has_toilet=request.form.get("toilet", "").lower() == "true",
        has_wifi=request.form.get("wifi", "").lower() == "true",
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"Success": "Cafes added successfully!"})


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_price(cafe_id):
    new_price = request.args.get("new_price")

    cafe = db.session.get(Cafe, cafe_id)

    if cafe is None:
        return jsonify(
            error="Sorry, we don't have a cafe with that id."
        ), 404

    if new_price is None:
        return jsonify(
            error="Please provide a new_price."
        ), 400

    cafe.coffee_price = new_price
    db.session.commit()

    return jsonify(
        response="Cafe updated successfully!",
        updated_cafe=cafe.to_dict()
    ), 200

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        try:
            cafe = db.session.get(Cafe, cafe_id)
            if cafe is None:
                raise ValueError("Cafe not found.")
        except AttributeError:
            return jsonify("Sorry a cafe with that id was not found in the database."), 404
        else:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify("Successfully deleted the cafe from the database."), 200
    else:
        return jsonify("Sorry, that's not allowed. Make sure you have the correct api_key."), 403

if __name__ == '__main__':
    app.run(debug=True)
