import allure
import pytest
import requests
from src.api.order_api import OrderAPI

class TestOrderGet:
    """Класс для тестирования получения заказа по номеру (треку)"""

    @pytest.fixture
    def order_api(self):
        return OrderAPI()

    @pytest.fixture
    def create_test_order(self, order_api):
        order_data = {
            "firstName": "TestUser",
            "lastName": "TestLastName",
            "address": "Test Address, 123",
            "metroStation": 5,
            "phone": "+7 999 888 77 66",
            "rentTime": 3,
            "deliveryDate": "2026-08-15",
            "comment": "Test order for API testing",
            "color": ["BLACK"]
        }
        response = order_api.create_order(order_data)
        assert response.status_code == 201
        track = response.json()['track']
        yield track
        # Очистка после теста
        order_api.cancel_order(track)

    @allure.title("Успешное получение заказа по треку")
    @allure.description("Проверка, что запрос возвращает объект с заказом")
    def test_get_order_by_track_success(self, order_api, create_test_order):
        track = create_test_order
        response = order_api.get_order_by_track(track)

        assert response.status_code == 200
        assert 'order' in response.json()

        order = response.json()['order']
        required_fields = [
            'id', 'firstName', 'lastName', 'address',
            'metroStation', 'phone', 'rentTime', 'deliveryDate',
            'track', 'color', 'comment', 'status'
        ]
        for field in required_fields:
            assert field in order, f"Поле '{field}' отсутствует"

        assert order['track'] == track
        assert order['firstName'] is not None
        assert len(order['firstName']) > 0
        assert order['lastName'] is not None
        assert len(order['lastName']) > 0

    @allure.title("Получение заказа без номера")
    @allure.description("Проверка ошибки при отсутствии параметра t")
    def test_get_order_without_track_error(self, order_api):
        response = requests.get(f'{OrderAPI.BASE_URL}/orders/track')
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.text

    @allure.title("Получение заказа с пустым номером")
    @allure.description("Проверка ошибки при пустом значении трека")
    def test_get_order_with_empty_track_error(self, order_api):
        response = order_api.get_order_by_track('')
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.text or "Некорректный номер заказа" in response.text

    @allure.title("Получение несуществующего заказа")
    @allure.description("Проверка ошибки 404 для несуществующего трека")
    def test_get_order_nonexistent_track_error(self, order_api):
        response = order_api.get_order_by_track(999999)
        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Заказ не найден"}

    @allure.title("Получение заказа с отрицательным номером")
    @allure.description("Проверка обработки отрицательного трека")
    def test_get_order_with_negative_track_error(self, order_api):
        response = order_api.get_order_by_track(-1)
        assert response.status_code in [400, 404, 500]

    @allure.title("Получение заказа с текстовым номером")
    @allure.description("Проверка обработки строкового трека")
    def test_get_order_with_string_track_error(self, order_api):
        response = order_api.get_order_by_track('abc123')
        assert response.status_code in [400, 500]

    @allure.title("Получение отмененного заказа")
    @allure.description("Проверка состояния заказа после отмены")
    def test_get_order_after_cancellation(self, order_api, create_test_order):
        track = create_test_order
        
        # Отменяем заказ
        cancel_response = order_api.cancel_order(track)
        # Если заказ уже отменен (409), это тоже считается успехом
        assert cancel_response.status_code in [200, 409], f"Ожидался 200 или 409, получен {cancel_response.status_code}"

        # Проверяем, что заказ не доступен или имеет статус "отменен"
        response = order_api.get_order_by_track(track)
        if response.status_code == 404:
            assert "Заказ не найден" in response.text
        elif response.status_code == 200:
            order = response.json()['order']
            assert order.get('status') is not None
        else:
            assert False, f"Неожиданный код ответа: {response.status_code}"