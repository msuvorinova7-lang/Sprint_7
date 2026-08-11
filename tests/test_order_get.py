import pytest
import requests
import allure
from src.api.order_api import OrderAPI

class TestOrderGet:
    """Класс для тестирования получения заказа по его номеру (треку)"""
    
    @pytest.fixture
    def order_api(self):
        return OrderAPI()
    
    @pytest.fixture
    def create_test_order(self, order_api):
        """
        Фикстура для создания тестового заказа
        Возвращает track (номер трека) созданного заказа
        """
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
        assert response.status_code == 201, "Заказ не был создан"
        track = response.json()['track']
        
        yield track
        
        # Очистка после теста
        order_api.cancel_order(track)
    
    @allure.title("Успешное получение заказа по треку")
    @allure.description("Проверка, что запрос возвращает объект с заказом")
    def test_get_order_by_track_success(self, order_api, create_test_order):
        """Тест: успешный запрос возвращает объект с заказом"""
        track = create_test_order
        
        response = order_api.get_order_by_track(track)
        
        assert response.status_code == 200, f"Код ответа должен быть 200, получен {response.status_code}"
        
        response_json = response.json()
        assert 'order' in response_json, "В ответе должен быть ключ 'order'"
        
        order = response_json['order']
        
        required_fields = [
            'id', 'firstName', 'lastName', 'address',
            'metroStation', 'phone', 'rentTime', 'deliveryDate',
            'track', 'color', 'comment', 'status'
        ]
        
        for field in required_fields:
            assert field in order, f"В заказе должно быть поле '{field}'"
        
        assert order['track'] == track, f"Трек заказа должен быть {track}, получен {order['track']}"
        
        # Проверяем, что firstName существует и не пустое
        assert 'firstName' in order, "В заказе должно быть поле firstName"
        assert order['firstName'] is not None, "firstName не должно быть None"
        assert len(order['firstName']) > 0, "firstName не должно быть пустым"
        
        # Проверяем lastName
        assert 'lastName' in order, "В заказе должно быть поле lastName"
        assert order['lastName'] is not None, "lastName не должно быть None"
        assert len(order['lastName']) > 0, "lastName не должно быть пустым"
    
    @allure.title("Получение заказа без номера")
    @allure.description("Проверка ошибки при запросе без номера заказа")
    def test_get_order_without_track_error(self, order_api):
        """Тест: запрос без номера заказа возвращает ошибку"""
        response = requests.get(f'{OrderAPI.BASE_URL}/orders/track')
        
        assert response.status_code == 400, f"Код ответа должен быть 400, получен {response.status_code}"
        assert "Недостаточно данных для поиска" in response.text
    
    @allure.title("Получение заказа с пустым номером")
    @allure.description("Проверка ошибки при запросе с пустым номером заказа")
    def test_get_order_with_empty_track_error(self, order_api):
        """Тест: запрос с пустым номером заказа возвращает ошибку"""
        response = order_api.get_order_by_track('')
        
        assert response.status_code == 400, f"Код ответа должен быть 400, получен {response.status_code}"
        assert "Недостаточно данных для поиска" in response.text or "Некорректный номер заказа" in response.text
    
    @allure.title("Получение несуществующего заказа")
    @allure.description("Проверка ошибки при запросе с несуществующим треком")
    def test_get_order_nonexistent_track_error(self, order_api):
        """Тест: запрос с несуществующим заказом возвращает ошибку"""
        response = order_api.get_order_by_track(999999)
        
        assert response.status_code == 404, f"Код ответа должен быть 404, получен {response.status_code}"
        assert response.json() == {"code": 404, "message": "Заказ не найден"}
    
    @allure.title("Получение заказа с отрицательным номером")
    @allure.description("Проверка ошибки при запросе с отрицательным треком")
    def test_get_order_with_negative_track_error(self, order_api):
        """Тест: запрос с отрицательным номером заказа"""
        response = order_api.get_order_by_track(-1)
        
        assert response.status_code in [400, 404, 500], \
            f"Код ответа должен быть ошибкой, получен {response.status_code}"
    
    @allure.title("Получение заказа с текстовым номером")
    @allure.description("Проверка ошибки при запросе с текстовым треком")
    def test_get_order_with_string_track_error(self, order_api):
        """Тест: запрос с текстовым номером заказа"""
        response = order_api.get_order_by_track('abc123')
        
        assert response.status_code in [400, 500], \
            f"Код ответа должен быть 400 или 500, получен {response.status_code}"
    
    @allure.title("Получение отмененного заказа")
    @allure.description("Проверка получения заказа после его отмены")
    def test_get_order_after_cancellation(self, order_api, create_test_order):
        """Тест: проверка получения заказа после его отмены"""
        track = create_test_order
        
        cancel_response = order_api.cancel_order(track)
        assert cancel_response.status_code == 200, "Заказ должен быть отменен"
        
        response = order_api.get_order_by_track(track)
        
        if response.status_code == 404:
            assert "Заказ не найден" in response.text
        elif response.status_code == 200:
            order = response.json()['order']
            assert order.get('status') is not None
        else:
            assert False, f"Неожиданный код ответа: {response.status_code}"