import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

df = pd.read_csv('/data/training_data.csv',
                  names=['ride_id', 'lat', 'lon', 'fare', 'timestamp', 'zone'],
                  header=None)
df = df[df['timestamp'] != 'timestamp']
df['timestamp'] = pd.to_numeric(df['timestamp'])
df['fare'] = pd.to_numeric(df['fare'])
df['ride_id'] = pd.to_numeric(df['ride_id'])
df['hour'] = pd.to_datetime(df['timestamp'], unit='s').dt.hour
df['dow'] = pd.to_datetime(df['timestamp'], unit='s').dt.dayofweek

agg = df.groupby(['zone', 'hour', 'dow']).agg(
    ride_count=('ride_id', 'count'),
    avg_fare=('fare', 'mean')
).reset_index()
agg['earnings_per_hour'] = agg['ride_count'] * agg['avg_fare']

X = pd.get_dummies(agg[['zone', 'hour', 'dow']], columns=['zone'])
y_demand = agg['ride_count']
y_earnings = agg['earnings_per_hour']


def train_and_select(X, y, target_name):
    models = {
        "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
        "LinearRegression": LinearRegression(),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    best_model = None
    best_score = -float('inf')
    best_name = None
    for name, model in models.items():
        model.fit(X_train, y_train)
        score = r2_score(y_test, model.predict(X_test))
        if score > best_score:
            best_score = score
            best_model = model
            best_name = name
    return best_model, best_name


demand_model, demand_best = train_and_select(X, y_demand, "Demand")
earnings_model, earnings_best = train_and_select(X, y_earnings, "Earnings")

print("demand id:", id(demand_model))
print("earnings id:", id(earnings_model))
print("SAME OBJECT:", demand_model is earnings_model)
print("demand pred row0:", demand_model.predict(X.iloc[[0]]))
print("earnings pred row0:", earnings_model.predict(X.iloc[[0]]))

joblib.dump(demand_model, '/data/demand_model.pkl')
joblib.dump(earnings_model, '/data/earnings_model.pkl')

import hashlib
with open('/data/demand_model.pkl','rb') as f1, open('/data/earnings_model.pkl','rb') as f2:
    h1 = hashlib.md5(f1.read()).hexdigest()
    h2 = hashlib.md5(f2.read()).hexdigest()
print("hash demand:", h1)
print("hash earnings:", h2)
print("FILES SAME:", h1 == h2)