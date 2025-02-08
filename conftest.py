import pytest
from api_client import ApiClient
from data import BASE_URL, COURIER_ENDPOINT, LOGIN_ENDPOINT
from helpers import generate_random_string
from courier_helper import register_new_courier_and_return_login_password
import json

@pytest.fixture(scope="session")
def api_client():
    return ApiClient(BASE_URL)

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
                return  # success
            else:
                print(f"Failed to delete courier: {delete_response.text}")
        else:
            print(f"Failed to get courier ID for deletion: {response.text}")
    else:
        pytest.fail("Failed to register courier")

