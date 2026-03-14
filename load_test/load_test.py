import requests
from concurrent.futures import ThreadPoolExecutor
import time

URL = "http://localhost:8000/events"

payload = {
    "user_id": "load_test_user",
    "event_type": "page_view",
    "metadata": {
        "page": "/test"
    }
}


def send_event():
    try:
        requests.post(URL, json=payload)
    except:
        pass


TOTAL_REQUESTS = 5000
WORKERS = 50

start = time.time()

with ThreadPoolExecutor(max_workers=WORKERS) as executor:
    for _ in range(TOTAL_REQUESTS):
        executor.submit(send_event)

end = time.time()

print("Load test complete")
print("Total requests:", TOTAL_REQUESTS)
print("Workers:", WORKERS)
print("Duration:", round(end-start,2),"seconds")
print("Requests/sec:", round(TOTAL_REQUESTS/(end-start),2))