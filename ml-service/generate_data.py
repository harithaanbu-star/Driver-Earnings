import pandas as pd
import random

zones = ["A", "B", "C", "D"]
rows = []

for dow in range(7):
    for hour in range(24):
        for zone in zones:
            # Make demand depend on hour and zone (realistic pattern)
            base_demand = 5
            if 7 <= hour <= 10 or 17 <= hour <= 21:  # peak hours
                base_demand += 10
            if zone in ["A", "C"]:  # busier zones
                base_demand += 5

            ride_count = max(1, int(random.gauss(base_demand, 2)))

            for _ in range(ride_count):
                fare = random.randint(80, 400)
                if 17 <= hour <= 21:
                    fare += 50  # evening surge pricing
                timestamp = 1781400000 + dow * 86400 + hour * 3600 + random.randint(0, 3599)
                rows.append({
                    "ride_id": random.randint(1000, 9999),
                    "lat": round(random.uniform(11.0, 11.1), 4),
                    "lon": round(random.uniform(76.9, 77.0), 4),
                    "fare": fare,
                    "timestamp": timestamp,
                    "zone": zone
                })

df = pd.DataFrame(rows)
df.to_csv('/data/training_data.csv', index=False, header=False)
print(f"Generated {len(df)} rows covering 7 days x 24 hours x 4 zones")