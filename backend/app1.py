
from flask import Flask, request, jsonify
import pandas as pd
import joblib
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS
CORS(app)


# Load trained model
model_data = joblib.load("ticket_price_model.pkl")

model = model_data["model"]
model_columns = model_data["columns"]


# Load dataset
df = pd.read_csv("dataset/airlines_flights_data.csv")


# Get unique values for dropdowns
airlines = sorted(df["airline"].unique().tolist())
source_cities = sorted(df["source_city"].unique().tolist())
destination_cities = sorted(df["destination_city"].unique().tolist())
classes = sorted(df["class"].unique().tolist())
departure_times = sorted(df["departure_time"].unique().tolist())
arrival_times = sorted(df["arrival_time"].unique().tolist())
stops = sorted(df["stops"].unique().tolist())


# API 1: Get dropdown options
@app.route("/api/options", methods=["GET"])
def get_options():

    return jsonify({
        "airlines": airlines,
        "source_cities": source_cities,
        "destination_cities": destination_cities,
        "classes": classes,
        "departure_times": departure_times,
        "arrival_times": arrival_times,
        "stops": stops
    })


# API 2: Predict ticket price
@app.route("/api/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        input_data = pd.DataFrame([{
            "airline": data["airline"],
            "source_city": data["source_city"],
            "destination_city": data["destination_city"],
            "class": data["travel_class"],
            "departure_time": data["departure_time"],
            "arrival_time": data["arrival_time"],
            "stops": data["stops"],
            "duration": float(data["duration"]),
            "days_left": int(data["days_left"])
        }])

        # Convert categorical data into numerical format
        input_encoded = pd.get_dummies(input_data, dtype=int)

        # Match training columns
        input_encoded = input_encoded.reindex(
            columns=model_columns,
            fill_value=0
        )

        # Predict ticket price
        prediction = model.predict(input_encoded)[0]

        return jsonify({
            "predicted_price": round(float(prediction), 2)
        })

    except (KeyError, TypeError, ValueError) as e:
        return jsonify({
            "error": str(e)
        }), 400


# Run Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)