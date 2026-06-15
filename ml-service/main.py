from fastapi import FastAPI
import joblib, pandas as pd
import os

app = FastAPI()

demand_model = None
earnings_model = None
model_columns = None

@app.on_event("startup")
def load_models():
    global demand_model, earnings_model, model_columns
    if os.path.exists('/data/demand_model.pkl'):
        demand_model = joblib.load('/data/demand_model.pkl')
        earnings_model = joblib.load('/data/earnings_model.pkl')
        model_columns = joblib.load('/data/model_columns.pkl')

@app.get("/predict")
def predict(hour: int, dow: int):
    if demand_model is None:
        return {"error": "Models not trained yet"}

    zones = ['A', 'B', 'C', 'D']
    results = []
    for z in zones:
        row = {col: 0 for col in model_columns}
        row['hour'] = hour
        row['dow'] = dow
        zone_col = f'zone_{z}'
        if zone_col in row:
            row[zone_col] = 1
        X = pd.DataFrame([row])[model_columns]
        demand = demand_model.predict(X)[0]
        earnings = earnings_model.predict(X)[0]
        results.append({
            "zone": z,
            "predicted_demand": round(float(demand), 1),
            "predicted_earnings_per_hour": round(float(earnings), 1)
        })
    return sorted(results, key=lambda x: -x['predicted_earnings_per_hour'])