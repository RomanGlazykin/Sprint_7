import pytest
import json

BASE_URL = "https://qa-scooter.praktikum-services.ru"
ORDER_ENDPOINT = "/api/v1/orders"

@pytest.fixture
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

@pytest.mark.parametrize("color", [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    [],
])
def test_create_order_with_different_colors(api_client, order_data, color):
    payload = order_data.copy()
    payload["color"] = color
    response = api_client.post(ORDER_ENDPOINT, data=payload)
    assert response is not None, "Order creation request failed"
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
    response_body = json.loads(response.text)
    assert "track" in response_body, "No 'track' in response body"

def test_get_order_list_no_courier_id(api_client):
    response = api_client.get(ORDER_ENDPOINT)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
    try:
        response_body = json.loads(response.text)
        assert isinstance(response_body, dict), "Response body is not a dict"
        assert "orders" in response_body, "No 'orders' key in response body"
        order_list = response_body["orders"]
        assert isinstance(order_list, list), "The value of 'orders' is not a list"
        if order_list:
            for order in order_list:
                assert isinstance(order, dict), "Each element in the list is not a dict"
                assert "id" in order, "Order has no 'id'"
                assert "courierId" in order, "Order has no 'courierId'"
                assert "firstName" in order, "Order has no 'firstName'"
                assert "lastName" in order, "Order has no 'lastName'"
                assert "address" in order, "Order has no 'address'"
                assert "metroStation" in order, "Order has no 'metroStation'"
                assert "phone" in order, "Order has no 'phone'"
                assert "rentTime" in order, "Order has no 'rentTime'"
                assert "deliveryDate" in order, "Order has no 'deliveryDate'"
                assert "track" in order, "Order has no 'track'"
                assert "color" in order, "Order has no 'color'"
                assert "comment" in order, "Order has no 'comment'"
                assert "createdAt" in order, "Order has no 'createdAt'"
                assert "updatedAt" in order, "Order has no 'updatedAt'"
                assert "status" in order, "Order has no 'status'"
        assert "pageInfo" in response_body, "No 'pageInfo' key in response body"
        page_info = response_body["pageInfo"]
        assert isinstance(page_info, dict), "'pageInfo' is not a dict"
        assert "page" in page_info, "'pageInfo' has no 'page' key"
        assert "total" in page_info, "'pageInfo' has no 'total' key"
        assert "limit" in page_info, "'pageInfo' has no 'limit' key"
        if "availableStations" in response_body:
            available_stations = response_body["availableStations"]
            assert isinstance(available_stations, list), "'availableStations' is not a list"
    except json.JSONDecodeError:
        pytest.fail("Response body is not JSON")