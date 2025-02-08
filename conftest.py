import pytest
from api_client import ApiClient
import string
import random
import json

BASE_URL = "https://qa-scooter.praktikum-services.ru/"
COURIER_ENDPOINT = "/api/v1/courier"
LOGIN_ENDPOINT = "/api/v1/courier/login"

@pytest.fixture(scope="session")
def api_client():
    return ApiClient(BASE_URL)

def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def register_new_courier_and_return_login_password(api_client):
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = api_client.post(COURIER_ENDPOINT, data=payload)

    if response and response.status_code == 201:
        return {"login": login, "password": password, "firstName": first_name}
    else:
        return None

@pytest.fixture()
def create_and_delete_courier(api_client):
    courier_data = register_new_courier_and_return_login_password(api_client)
    if courier_data:
        yield courier_data
        login_payload = {"login": courier_data["login"], "password": courier_data["password"]}
        response = api_client.post(LOGIN_ENDPOINT, data=login_payload)
        if response and response.status_code == 200:
            courier_id = json.loads(response.text)["id"]
            delete_response = api_client.delete(f"{COURIER_ENDPOINT}/{courier_id}")
            if delete_response and delete_response.status_code == 200:
                return # success
            else:
                print(f"Failed to delete courier: {delete_response.text}")
        else:
            print(f"Failed to get courier ID for deletion: {response.text}")
    else:
        pytest.fail("Failed to register courier")

@pytest.fixture()
def order_data():
    return {
        "firstName": "Naruto",
        "lastName": "Uzumaki",
        "address": "Konoha, 12",
        "metroStation": 4,
        "phone": "+78003553535",
        "rentTime": 5,
        "deliveryDate": "2024-03-02",
        "comment": "Be quick!",
    }
