from kafka import KafkaProducer
import json, random, time

producer = KafkaProducer(
    bootstrap_servers='kafka:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

zones = ["A", "B", "C", "D"]

print("Producer started, sending ride events...")

while True:
    event = {
        "ride_id": random.randint(1000, 9999),
        "lat": round(random.uniform(11.0, 11.1), 4),
        "lon": round(random.uniform(76.9, 77.0), 4),
        "fare": random.randint(80, 400),
        "timestamp": time.time(),
        "zone": random.choice(zones)
    }
    producer.send('ride-events', event)
    print("Sent:", event)
    time.sleep(2)