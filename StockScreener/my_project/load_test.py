import requests
import time

URL = "http://127.0.0.1:8000/query"

total_requests = 50
times = []

for i in range(total_requests):
    start = time.time()

    res = requests.post(URL, json={
        "query": "price > 400"
    })

    end = time.time()

    response_time = end - start
    times.append(response_time)

    print(f"Request {i+1}: {response_time:.4f} sec")

avg_time = sum(times) / len(times)

print("\nAverage Response Time:", avg_time)
print("Max Time:", max(times))
print("Min Time:", min(times))