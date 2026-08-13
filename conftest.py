import pytest

from src.helpers.courier_helpers import CourierHelpers
from src.api.order_api import OrderAPI


@pytest.fixture
def courier_helpers():
    helpers = CourierHelpers()

    courier_data = helpers.register_new_courier()

    yield helpers, courier_data

    courier_id = helpers.get_courier_id(
        courier_data["login"],
        courier_data["password"]
    )

    if courier_id:
        helpers.delete_courier(courier_id)


@pytest.fixture
def order_api():
    return OrderAPI()