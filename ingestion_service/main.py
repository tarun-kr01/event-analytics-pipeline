from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
import uuid
from datetime import datetime
import time
import logging
from fastapi import Request

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("metrics")

# connect to redis queue
redis_client = redis.Redis(host="localhost", port=6379, db=0)

QUEUE_NAME = "event_queue"


class Event(BaseModel):
    user_id: str
    event_type: str
    metadata: dict | None = None

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

@app.post("/events")
async def ingest_event(event: Event):

    event_payload = {
        "event_id": str(uuid.uuid4()),
        "user_id": event.user_id,
        "event_type": event.event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": event.metadata or {}
    }

    redis_client.rpush(QUEUE_NAME, json.dumps(event_payload))

    return {
        "status": "queued",
        "event_id": event_payload["event_id"]
    }