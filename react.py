from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = MongoClient("mongodb://localhost:27017/")
db = client["dual-zone-meter"]
readings_collection = db["meter_readings"]
meters_collection = db["meters"]

AVAILABLE_METERS = ["M001", "M002", "M003"]
ERROR_DAY = 100;
ERROR_NIGHT = 80;

@app.route("/", methods=["GET", "POST"])
def index():
    selected_meter = request.args.get("meter_id", "M001")

    if selected_meter not in AVAILABLE_METERS:
        flash("Невідомий лічильник!", "error")
        return redirect("/")

    latest = readings_collection.find_one({"meter_id": selected_meter}, sort=[("submitted_at", -1)])

    if not latest:
        latest = {
            "day": 0,
            "night": 0,
            "total_kwh": 0,
            "total_amount": 0.0,
            "delta_day": 0,
            "delta_night": 0,
            "delta_kwh": 0,
            "delta_amount": 0.0
        }

    current_reading = latest
    coefficient_day = 4.32  # Тариф для дня
    coefficient_night = 2.16  # Тариф для ночі
    temp_data = None

    all_readings = list(readings_collection.find({"meter_id": selected_meter}))
    total_day_all = sum(r["day"] for r in all_readings)
    total_night_all = sum(r["night"] for r in all_readings)
    total_kwh_all = total_day_all + total_night_all
    total_amount_all = round(sum(r["total_amount"] for r in all_readings), 2)

    if request.method == "POST":
        try:
            day = int(request.form["day"])
            night = int(request.form["night"])
            delta_day = day - latest["day"]
            delta_night = night - latest["night"]

            # Якщо введені значення менші за попередні — робимо накрутку
            if delta_day < 0 or delta_night < 0:
                new_day = latest["day"] + ERROR_DAY
                new_night = latest["night"] + ERROR_NIGHT
                delta_day = ERROR_DAY
                delta_night = ERROR_NIGHT
                flash("",
                      "warning")
            else:
                new_day = day
                new_night = night
                delta_day = new_day - latest["day"]
                delta_night = new_night - latest["night"]

            delta_kwh = delta_day + delta_night
            delta_amount = round((delta_day * coefficient_day) + (delta_night * coefficient_night), 2)

            reading = {
                "meter_id": selected_meter,
                "day": new_day,
                "night": new_night,
                "coefficient_day": coefficient_day,
                "coefficient_night": coefficient_night,
                "submitted_at": datetime.utcnow(),
                "total_kwh": new_day + new_night,
                "total_amount": round((new_day * coefficient_day) + (new_night * coefficient_night), 2),
                "delta_day": delta_day,
                "delta_night": delta_night,
                "delta_kwh": delta_kwh,
                "delta_amount": delta_amount
            }
            readings_collection.insert_one(reading)

            meters_collection.update_one(
                {"meter_id": selected_meter},
                {
                    "$inc": {
                        "total_day": delta_day,
                        "total_night": delta_night,
                        "total_kwh": delta_kwh,
                        "total_amount": delta_amount
                    },
                    "$set": {
                        "last_updated": datetime.utcnow()
                    }
                },
                upsert=True
            )

            flash("Дані успішно додано!", "success")
            return redirect(f"/?meter_id={selected_meter}")

        except Exception as e:
            flash(f"Помилка: {e}", "error")

    meter_stats = meters_collection.find_one({"meter_id": selected_meter})
    if not meter_stats:
        meter_stats = {
            "total_day": 0,
            "total_night": 0,
            "total_kwh": 0,
            "total_amount": 0.0
        }

    return render_template(
        "index.html",
        reading=current_reading,
        temp=temp_data,
        selected_meter=selected_meter,
        meters=AVAILABLE_METERS,
        total_day_all=meter_stats["total_day"],
        total_night_all=meter_stats["total_night"],
        total_kwh_all=meter_stats["total_kwh"],
        total_amount_all=meter_stats["total_amount"]
    )


if __name__ == "__main__":
    app.run(debug=True)