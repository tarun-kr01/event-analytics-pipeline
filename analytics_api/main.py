from fastapi import FastAPI
import psycopg2
import redis
import json
import time
import logging
from fastapi import Request

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("metrics")

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="events",
    user="admin",
    password="password"
)

cursor = conn.cursor()

# Redis cache connection
cache = redis.Redis(host="localhost", port=6379, db=1)

CACHE_TTL = 60

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"endpoint={request.url.path} "
        f"method={request.method} "
        f"status={response.status_code} "
        f"latency_ms={round(process_time*1000,2)}"
    )

    return response

@app.get("/metrics/events")
def total_events():

    cached = cache.get("total_events")

    if cached:
        return json.loads(cached)

    cursor.execute("SELECT COUNT(*) FROM events")
    count = cursor.fetchone()[0]

    result = {"total_events": count}

    cache.setex("total_events", CACHE_TTL, json.dumps(result))

    return result


@app.get("/metrics/active-users")
def active_users():

    cached = cache.get("active_users")

    if cached:
        return json.loads(cached)

    cursor.execute(
        "SELECT COUNT(DISTINCT event_data->>'user_id') FROM events"
    )

    users = cursor.fetchone()[0]

    result = {"active_users": users}

    cache.setex("active_users", CACHE_TTL, json.dumps(result))

    return result


@app.get("/metrics/events-by-type")
def events_by_type():

    cached = cache.get("events_by_type")

    if cached:
        return json.loads(cached)

    cursor.execute("""
        SELECT
        event_data->>'event_type',
        COUNT(*)
        FROM events
        GROUP BY event_data->>'event_type'
    """)

    rows = cursor.fetchall()

    result = {}

    for r in rows:
        result[r[0]] = r[1]

    cache.setex("events_by_type", CACHE_TTL, json.dumps(result))

    return result