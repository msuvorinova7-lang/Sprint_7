import pytest

from src.api.order_api import OrderAPI
from src.data.order_data import OrderData
from src.helpers.courier_helpers import CourierHelpers


@pytest.fixture
def order_api():
    return OrderAPI()


@pytest.fixture
def courier_helpers():
    helpers = CourierHelpers()

    courier_data = helpers.register_new_courier()

    courier_id = helpers.get_courier_id(
        courier_data["login"],
        courier_data["password"]
    )

    yield helpers, courier_data, courier_id

    helpers.delete_courier(courier_id)


@pytest.fixture
def create_test_order(order_api):
    response = order_api.create_order(
        OrderData.ORDER_DATA.copy()
    )

    assert response.status_code == 201

    return response.json()["track"]