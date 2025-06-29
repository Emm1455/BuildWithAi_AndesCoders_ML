from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
from supabase import create_client
from datetime import datetime
import os

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Supabase setup
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set.")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    body = request.json
    X = pd.DataFrame([{
    "humidity": body["humidity"],
    "temperature": body["temperature"]
    }])

    prediction = model.predict(X)[0].tolist()

    # Save to Supabase
    try:
        res = supabase.table("predictions").insert({
            "temperaturainput": body["temperature"],
            "humedadinput": body["humidity"],
            "motorpwm1": prediction[0],
            "motorpwm2": prediction[1],
            "ph": 6,
            "altura": 7,
            "t": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nombre": 1,
        }).execute()
        print("Supabase insert OK", res)
    except Exception as e:
        print("❌ Supabase insert failed:", e)

    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)