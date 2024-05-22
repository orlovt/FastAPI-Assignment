import requests
import json
import time

url = "http://127.0.0.1:8000/log"
headers = {
    "Content-Type": "application/json"
}

for i in range(50):
    payload = {
        "message": f"New entry {i}",
        "level": "INFO"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Sent log {i}: Status Code {response.status_code}")
    time.sleep(0.1)