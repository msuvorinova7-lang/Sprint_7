import pytest

from src.api.order_api import OrderAPI
from src.data.order_data import OrderData
from src.helpers.courier_helpers import CourierHelpers


@pytest.fixture
def order_api():
    """Возвращает объект для работы с API заказов."""
    return OrderAPI()


@pytest.fixture
def courier_helpers():
    """
    Создаёт курьера перед тестом
    и удаляет его после завершения теста.
    """
    helpers = CourierHelpers()

    courier_data = helpers.register_new_courier()

    if courier_data is None:
        raise RuntimeError("Не удалось создать тестового курьера")

    courier_id = helpers.get_courier_id(
        courier_data["login"],
        courier_data["password"]
    )

    yield helpers, courier_data, courier_id

    helpers.delete_courier(courier_id)


@pytest.fixture
def create_test_order(order_api):
    """
    Создаёт тестовый заказ перед тестом
    и отменяет его после завершения теста.
    """
    response = order_api.create_order(
        OrderData.ORDER_DATA.copy()
    )

    track = response.json()["track"]

    yield track

    order_api.cancel_order(track)
