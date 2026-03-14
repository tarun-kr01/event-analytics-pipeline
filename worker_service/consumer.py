import redis
import psycopg2
import json

redis_client = redis.Redis(host="localhost", port=6379, db=0)

conn = psycopg2.connect(
    host="localhost",
    database="events",
    user="admin",
    password="password"
)

cursor = conn.cursor()

QUEUE_NAME = "event_queue"

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

print("Worker started. Waiting for events...")

while True:
    event = redis_client.blpop(QUEUE_NAME)

    if event:
        event_data = json.loads(event[1])

        cursor.execute(
            "INSERT INTO events (event_data) VALUES (%s)",
            [json.dumps(event_data)]
        )

        conn.commit()

        print("Event stored:", event_data["event_id"])