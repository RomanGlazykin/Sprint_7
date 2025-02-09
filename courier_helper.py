from api_client import ApiClient
from helpers import generate_random_string

def register_new_courier_and_return_login_password(api_client: ApiClient):
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = api_client.post("/api/v1/courier", data=payload)

    if response and response.status_code == 201:
        return {"login": login, "password": password, "firstName": first_name}
    else:
        return None