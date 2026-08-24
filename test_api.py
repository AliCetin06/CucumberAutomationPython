import requests

BASE_URL = "http://127.0.0.1:8000"


def test_get_item_details():
    # 1. İsteği Gönder (GET)
    response = requests.get(f"{BASE_URL}/items/1")

    # 2. Durum Kodunu Doğrula (Status Code 200)
    assert response.status_code == 200

    # 3. Gelen JSON Verisini Doğrula
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99


def test_create_new_item():
    # 1. Gönderilecek Veriyi Hazırla (Body)
    payload = {
        "name": "Tablet",
        "price": 299.99
    }

    # 2. İsteği Gönder (POST)
    response = requests.post(f"{BASE_URL}/items/", json=payload)

    # 3. Doğrulamaları Yap
    assert response.status_code == 200

    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Tablet"
