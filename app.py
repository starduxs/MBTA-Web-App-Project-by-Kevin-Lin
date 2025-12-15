from flask import Flask, render_template, request
import mbta_helper

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    place = request.form.get("place")

    try:
        station, wheelchair = mbta_helper.find_stop_near(place)
        return render_template(
            "mbta_station.html",
            place=place,
            station=station,
            wheelchair=wheelchair
        )
    except Exception:
        return render_template("index.html", error="Could not find a nearby station.")


if __name__ == "__main__":
    app.run(debug=True)
