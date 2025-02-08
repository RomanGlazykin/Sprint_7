import pytest
import json

BASE_URL = "https://qa-scooter.praktikum-services.ru"
COURIER_ENDPOINT = "/api/v1/courier"
LOGIN_ENDPOINT = "/api/v1/courier/login"


def create_courier(api_client, courier_data):
    response = api_client.post(COURIER_ENDPOINT, data=courier_data)
    assert response is not None, "Courier creation request failed"
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
    assert json.loads(response.text) == {"ok": True}, f"Unexpected response body: {response.text}"
    return response
def test_create_courier_success(api_client, create_and_delete_courier):
    pass
def test_create_duplicate_courier(api_client, create_and_delete_courier):
    response = api_client.post(COURIER_ENDPOINT, data=create_and_delete_courier)
    assert response is not None, "Second courier creation request failed"
    assert response.status_code == 409, f"Unexpected status code for duplicate courier: {response.status_code}, Response text: {response.text}"

    try:
        response_body = json.loads(response.text)
        assert "message" in response_body, "No error message in response"
    except json.JSONDecodeError:
        print("Response body is not JSON, cannot check error message")


@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_create_courier_without_required_field(api_client, create_and_delete_courier, missing_field):
    payload = create_and_delete_courier.copy()
    del payload[missing_field]
    response = api_client.post(COURIER_ENDPOINT, data=payload)

    assert response is not None, "Request failed"
    assert response.status_code == 400, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
    try:
        response_body = json.loads(response.text)
        assert "message" in response_body, "No error message in response"
        assert "message" in json.loads(response.text)
    except json.JSONDecodeError:
        print("Response body is not JSON, cannot check error message")

def create_login_payload(login, password):
    return {
        "login": login,
        "password": password
    }

def test_courier_can_login(api_client, create_and_delete_courier):
    login_payload = create_login_payload(create_and_delete_courier["login"], create_and_delete_courier["password"])
    response = api_client.post(LOGIN_ENDPOINT, data=login_payload)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
    response_body = json.loads(response.text)
    assert "id" in response_body, "No 'id' in response body"

@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_courier_login_without_required_fields(api_client, create_and_delete_courier, missing_field):

    login_payload = create_login_payload(create_and_delete_courier["login"], create_and_delete_courier["password"])
    login_payload[missing_field] = ""

    response = api_client.post(LOGIN_ENDPOINT, data=login_payload)

    assert response is not None, "Request timed out or failed"
    assert response.status_code == 400, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
    response_body = json.loads(response.text)
    assert "message" in response_body, "No error message in response"
    assert response_body["message"] == "Недостаточно данных для входа"

@pytest.mark.parametrize("wrong_field", ["login", "password"])
def test_courier_login_with_wrong_credentials(api_client, create_and_delete_courier, wrong_field):
    login_payload = {
        "login": create_and_delete_courier["login"],
        "password": create_and_delete_courier["password"]
    }
    if wrong_field == "login":
        login_payload["login"] = "wrong_login"
    elif wrong_field == "password":
        login_payload["password"] = "wrong_password"

    response = api_client.post(LOGIN_ENDPOINT, data=login_payload)

    assert response.status_code == 404, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
    response_body = json.loads(response.text)
    assert "message" in response_body, "No error message in response"
    assert response_body["message"] == "Учетная запись не найдена"

def test_courier_login_non_existing_user(api_client):
    login_payload = {
        "login": "non_existing_login",
        "password": "non_existing_password"
    }

    response = api_client.post(LOGIN_ENDPOINT, data=login_payload)

    assert response.status_code == 404, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
    response_body = json.loads(response.text)
    assert "message" in response_body, "No error message in response"
    assert response_body["message"] == "Учетная запись не найдена"

def test_courier_can_login_returns_id(api_client, create_and_delete_courier):
    login_payload = create_login_payload(create_and_delete_courier["login"], create_and_delete_courier["password"])
    response = api_client.post(LOGIN_ENDPOINT, data=login_payload)

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
    response_body = json.loads(response.text)
    assert "id" in response_body, "No 'id' in response body"
    assert type(response_body["id"]) == int, "ID must be integer"
