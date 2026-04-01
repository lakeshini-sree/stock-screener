import requests

BASE_URL = "http://127.0.0.1:8000"

def test_query_api():
    res = requests.post(f"{BASE_URL}/query", json={
        "query": "price > 400"
    })

    data = res.json()

    assert res.status_code == 200
    assert data["status"] == "success"