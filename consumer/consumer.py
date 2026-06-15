from kafka import KafkaConsumer
import json, pandas as pd, os

consumer = KafkaConsumer(
    'ride-events',
    bootstrap_servers='kafka:29092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='consumer-group-1'
)

print("Consumer started, listening for ride events...")

records = []
output_file = '/data/training_data.csv'

for msg in consumer:
    records.append(msg.value)
    print("Received:", msg.value)

    if len(records) >= 10:
        df = pd.DataFrame(records)
        file_exists = os.path.isfile(output_file)
        df.to_csv(output_file, mode='a', index=False, header=not file_exists)
        print(f"Saved {len(records)} records to {output_file}")
        records = []