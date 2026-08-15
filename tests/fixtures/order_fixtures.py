import pytest

from src.data.order_data import OrderData


@pytest.fixture
def create_test_order(order_api):
    response = order_api.create_order(OrderData.ORDER_DATA.copy())

    assert response.status_code == 201

    return response.json()["track"]