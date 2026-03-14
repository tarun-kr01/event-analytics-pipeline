import requests
import random
import time
from faker import Faker

fake = Faker()

URL = "http://localhost:8000/events"

event_types = [
    "page_view",
    "click",
    "login",
    "logout",
    "add_to_cart",
    "purchase"
]

def generate_event():
    return {
        "user_id": f"user_{random.randint(1,1000)}",
        "event_type": random.choice(event_types),
        "metadata": {
            "page": fake.uri_path(),
            "device": random.choice(["mobile","desktop","tablet"])
        }
    }


while True:

    event = generate_event()

    try:
        requests.post(URL, json=event)
    except:
        pass

    time.sleep(0.01)