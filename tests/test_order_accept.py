import allure
import pytest
import requests

from src.helpers.courier_helpers import CourierHelpers
from src.api.order_api import OrderAPI
from src.data.order_data import OrderData


class TestOrderAccept:
    """Класс для тестирования принятия заказа"""

    @pytest.fixture
    def helpers(self):
        return CourierHelpers()

    @pytest.fixture
    def order_api(self):
        return OrderAPI()

    @allure.title("Успешное принятие заказа курьером")
    @allure.description("Проверка, что заказ успешно принимается курьером")
    def test_accept_order_success(self, helpers, order_api):
        # Создаём курьера
        courier_data = helpers.register_new_courier()

        courier_id = helpers.get_courier_id(
            courier_data['login'],
            courier_data['password']
        )

        # Создаём заказ
        order_data = OrderData.get_order_data()
        create_response = order_api.create_order(order_data)

        track = create_response.json()['track']

        order_response = order_api.get_order_by_track(track)
        order_id = order_response.json()['order']['id']

        # Принимаем заказ
        response = order_api.accept_order(order_id, courier_id)

        # Проверяем результат теста
        assert response.status_code == 200, "Заказ не принят"
        assert response.json() == {"ok": True}, "Ответ не содержит ok:true"

        # Очистка
        helpers.delete_courier(courier_id)

    @allure.title("Принятие заказа без id курьера")
    @allure.description("Проверка ошибки при отсутствии courierId")
    def test_accept_order_without_courier_id(self, helpers, order_api):
        # Создаём заказ
        order_data = OrderData.get_order_data()
        create_response = order_api.create_order(order_data)

        track = create_response.json()['track']

        order_response = order_api.get_order_by_track(track)
        order_id = order_response.json()['order']['id']

        # Пытаемся принять без courierId
        response = requests.put(
            f'{order_api.BASE_URL}/orders/accept/{order_id}'
        )

        # Проверяем результат
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.text

        # Очистка
        order_api.cancel_order(track)

    @allure.title("Принятие заказа с неверным id курьера")
    @allure.description("Проверка ошибки при передаче несуществующего courierId")
    def test_accept_order_invalid_courier_id(self, helpers, order_api):
        # Создаём заказ
        order_data = OrderData.get_order_data()
        create_response = order_api.create_order(order_data)

        track = create_response.json()['track']

        order_response = order_api.get_order_by_track(track)
        order_id = order_response.json()['order']['id']

        # Пытаемся принять с неверным courierId
        response = order_api.accept_order(order_id, 999999)

        # Проверяем результат
        assert response.status_code == 404
        assert "Курьера с таким id не существует" in response.text

        # Очистка
        order_api.cancel_order(track)

    @allure.title("Принятие заказа с неверным id заказа")
    @allure.description("Проверка ошибки при передаче несуществующего orderId")
    def test_accept_order_invalid_order_id(self, helpers, order_api):
        # Создаём курьера
        courier_data = helpers.register_new_courier()

        courier_id = helpers.get_courier_id(
            courier_data['login'],
            courier_data['password']
        )

        # Пытаемся принять несуществующий заказ
        response = order_api.accept_order(999999, courier_id)

        # Проверяем результат
        assert response.status_code == 404
        assert "Заказа с таким id не существует" in response.text

        # Очистка
        helpers.delete_courier(courier_id)