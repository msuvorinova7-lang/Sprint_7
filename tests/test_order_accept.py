import allure
import pytest

from src.helpers.courier_helpers import CourierHelpers
from src.api.order_api import OrderAPI
from src.data.order_data import OrderData


class TestOrderAccept:
    """Тесты принятия заказа"""

    @pytest.fixture
    def helpers(self):
        return CourierHelpers()

    @pytest.fixture
    def order_api(self):
        return OrderAPI()

    @allure.title("Успешное принятие заказа курьером")
    @allure.description("Проверка успешного принятия заказа курьером")
    def test_accept_order_success(self, helpers, order_api):
        """Проверка успешного принятия заказа"""

        courier_data = helpers.register_new_courier()

        courier_id = helpers.get_courier_id(
            courier_data['login'],
            courier_data['password']
        )

        order_data = OrderData.get_order_data()
        create_response = order_api.create_order(order_data)

        track = create_response.json()['track']

        order_response = order_api.get_order_by_track(track)
        order_id = order_response.json()['order']['id']

        response = order_api.accept_order(order_id, courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

        helpers.delete_courier(courier_id)

    @allure.title("Принятие заказа без id курьера")
    @allure.description("Проверка ошибки при отсутствии courierId")
    def test_accept_order_without_courier_id(self, order_api):
        """Проверка принятия заказа без id курьера"""

        order_data = OrderData.get_order_data()
        create_response = order_api.create_order(order_data)

        track = create_response.json()['track']

        order_response = order_api.get_order_by_track(track)
        order_id = order_response.json()['order']['id']

        response = order_api.accept_order(order_id, None)

        assert response.status_code == 400

    @allure.title("Принятие заказа с неверным id курьера")
    @allure.description("Проверка ошибки с несуществующим courierId")
    def test_accept_order_invalid_courier_id(self, order_api):
        """Проверка принятия заказа с неверным id курьера"""

        order_data = OrderData.get_order_data()
        create_response = order_api.create_order(order_data)

        track = create_response.json()['track']

        order_response = order_api.get_order_by_track(track)
        order_id = order_response.json()['order']['id']

        response = order_api.accept_order(order_id, 999999)

        assert response.status_code == 404

    @allure.title("Принятие несуществующего заказа")
    @allure.description("Проверка ошибки с несуществующим orderId")
    def test_accept_order_invalid_order_id(self, helpers, order_api):
        """Проверка принятия несуществующего заказа"""

        courier_data = helpers.register_new_courier()

        courier_id = helpers.get_courier_id(
            courier_data['login'],
            courier_data['password']
        )

        response = order_api.accept_order(999999, courier_id)

        assert response.status_code == 404

        helpers.delete_courier(courier_id)