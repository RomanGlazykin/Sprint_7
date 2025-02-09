import pytest
import json
from courier_api import create_courier, create_login_payload
from data import COURIER_ENDPOINT, LOGIN_ENDPOINT, INSUFFICIENT_DATA_MESSAGE, DUPLICATE_LOGIN_MESSAGE, ACCOUNT_NOT_FOUND_MESSAGE
from helpers import generate_random_string


class TestCourier:
    def test_create_courier_success(self, api_client):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        courier_data = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = create_courier(api_client, courier_data)

        assert response.status_code == 201, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
        response_body = json.loads(response.text)
        assert response_body == {"ok": True}, f"Unexpected response body: {response_body}"

    def test_create_duplicate_courier(self, api_client, create_and_delete_courier):
        response = api_client.post(COURIER_ENDPOINT, data=create_and_delete_courier)
        assert response is not None, "Second courier creation request failed"
        assert response.status_code == 409, f"Unexpected status code for duplicate courier: {response.status_code}, Response text: {response.text}"

        response_body = json.loads(response.text)
        assert "message" in response_body, "No error message in response"
        assert response_body["message"] == DUPLICATE_LOGIN_MESSAGE

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field(self, api_client, create_and_delete_courier, missing_field):
        payload = create_and_delete_courier.copy()
        del payload[missing_field]
        response = api_client.post(COURIER_ENDPOINT, data=payload)

        assert response is not None, "Request failed"
        assert response.status_code == 400, f"Unexpected status code: {response.status_code}, Response text: {response.text}"

        response_body = json.loads(response.text)
        assert "message" in response_body, "No error message in response"
        assert "message" in json.loads(response.text)

    def test_courier_can_login(self, api_client, create_and_delete_courier):
        login_payload = create_login_payload(create_and_delete_courier["login"], create_and_delete_courier["password"])
        response = api_client.post(LOGIN_ENDPOINT, data=login_payload)

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
        response_body = json.loads(response.text)
        assert "id" in response_body, "No 'id' in response body"

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_courier_login_without_required_fields(self, api_client, create_and_delete_courier, missing_field):
        login_payload = create_login_payload(create_and_delete_courier["login"], create_and_delete_courier["password"])
        login_payload[missing_field] = ""

        response = api_client.post(LOGIN_ENDPOINT, data=login_payload)

        assert response is not None, "Request timed out or failed"
        assert response.status_code == 400, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
        response_body = json.loads(response.text)
        assert "message" in response_body, "No error message in response"
        assert response_body["message"] == INSUFFICIENT_DATA_MESSAGE

    @pytest.mark.parametrize(
        "login, password",
        [
            ("wrong_login", "omlvkhbiin"),
            ("uozfedbduu", "wrong_password"),
        ],
    )
    def test_courier_login_with_wrong_credentials(self, api_client, login, password):
        login_payload = {
            "login": login,
            "password": password
        }

        response = api_client.post(LOGIN_ENDPOINT, data=login_payload)

        assert response.status_code == 404, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
        response_body = json.loads(response.text)
        assert "message" in response_body, "No error message in response"
        assert response_body["message"] == ACCOUNT_NOT_FOUND_MESSAGE

    def test_courier_login_non_existing_user(self, api_client):
        login_payload = {
            "login": "non_existing_login",
            "password": "non_existing_password"
        }

        response = api_client.post(LOGIN_ENDPOINT, data=login_payload)

        assert response.status_code == 404, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
        response_body = json.loads(response.text)
        assert "message" in response_body, "No error message in response"
        assert response_body["message"] == ACCOUNT_NOT_FOUND_MESSAGE

    def test_courier_can_login_returns_id(self, api_client, create_and_delete_courier):
        login_payload = create_login_payload(create_and_delete_courier["login"], create_and_delete_courier["password"])
        response = api_client.post(LOGIN_ENDPOINT, data=login_payload)

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
        response_body = json.loads(response.text)
        assert "id" in response_body, "No 'id' in response body"
        assert type(response_body["id"]) == int, "ID must be integer"
