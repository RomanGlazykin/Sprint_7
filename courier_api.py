from data import COURIER_ENDPOINT


def create_courier(api_client, courier_data):
    response = api_client.post(COURIER_ENDPOINT, data=courier_data)
    assert response is not None, "Courier creation request failed"
    return response


def create_login_payload(login, password):
    return {
        "login": login,
        "password": password
    }