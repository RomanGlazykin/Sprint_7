import pytest
import json
from models import Order  # Импорт из корневой директории
from data import ORDER_DATA, ORDER_ENDPOINT

class TestOrder:
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        [],
    ])
    def test_create_order_with_different_colors(self, api_client, color):
        payload = ORDER_DATA.copy()
        payload["color"] = color
        response = api_client.post(ORDER_ENDPOINT, data=payload)
        assert response is not None, "Order creation request failed"
        assert response.status_code == 201, f"Unexpected status code: {response.status_code}, Response text: {response.text}"
        response_body = json.loads(response.text)
        assert "track" in response_body, "No 'track' in response body"

    def test_get_order_list(self, api_client): # Удалили order_payload из параметров
        #create order
        response_create = api_client.post(ORDER_ENDPOINT, data=ORDER_DATA) # Используем ORDER_DATA
        assert response_create.status_code == 201

        #get order list
        response = api_client.get(ORDER_ENDPOINT)
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response text: {response.text}"

        response_body = response.json()
        orders = [Order(order_data) for order_data in response_body['orders']]

        # Основные проверки
        assert isinstance(orders, list), "The value of 'orders' is not a list"
        assert len(orders) > 0, "The list of orders is empty"  # Проверяем, что список не пуст

        # Проверяем, что все элементы списка - объекты Order
        for order in orders:
            assert isinstance(order, Order), "Each element in the list is not an Order object"
            order.validate_fields()  # Валидируем поля каждого объекта Order