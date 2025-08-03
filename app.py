from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)
model_path = "model/music_boost_model.pkl"

if os.path.exists(model_path):
    model, scaler, features = joblib.load(model_path)
else:
    model = scaler = features = None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST" and model:
        try:
            data = [
                float(request.form["session_length"]),
                float(request.form["time_on_track"]),
                float(request.form["track_duration"]),
                float(request.form["energy"]),
                float(request.form["tempo"]),
                int(request.form["repeat_count"])
            ]
            df = pd.DataFrame([data], columns=features)
            df_scaled = scaler.transform(df)
            prediction = model.predict(df_scaled)[0]
            result = "Prediction: Skipped 🎵" if prediction == 1 else "Prediction: Played 🎶"
        except Exception as e:
            result = f"Error: {e}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

