import pytest
import requests
from src.helpers.courier_helpers import CourierHelpers
from src.api.order_api import OrderAPI

class TestOrderAccept:
    """Класс для тестирования принятия заказа (ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ)"""
    
    @pytest.fixture
    def helpers(self):
        return CourierHelpers()
    
    @pytest.fixture
    def order_api(self):
        return OrderAPI()
    
    def test_accept_order_success(self, helpers, order_api):
        """
        Тест 1: успешное принятие заказа
        Проверяет: успешный запрос возвращает {"ok":true}
        """
        # Создаем курьера
        courier_data = helpers.register_new_courier()
        assert courier_data is not None
        courier_id = helpers.get_courier_id(courier_data['login'], courier_data['password'])
        assert courier_id is not None
        
        # Создаем заказ
        order_data = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-08-09",
            "comment": "Test order",
            "color": ["BLACK"]
        }
        create_response = order_api.create_order(order_data)
        assert create_response.status_code == 201
        track = create_response.json()['track']
        
        # Получаем id заказа
        order_response = order_api.get_order_by_track(track)
        assert order_response.status_code == 200
        order_id = order_response.json()['order']['id']
        
        # Принимаем заказ
        response = order_api.accept_order(order_id, courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}
        
        # Очистка: удаляем только курьера (заказ нельзя отменить после принятия)
        helpers.delete_courier(courier_id)
        print(f"✅ Заказ {order_id} принят курьером {courier_id}")
    
    def test_accept_order_without_courier_id(self, helpers, order_api):
        """
        Тест 2: если не передать id курьера, запрос вернёт ошибку
        Проверяет: код 400
        """
        # Создаем заказ
        order_data = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-08-09",
            "comment": "Test order",
            "color": ["BLACK"]
        }
        create_response = order_api.create_order(order_data)
        assert create_response.status_code == 201
        track = create_response.json()['track']
        
        # Получаем id заказа
        order_response = order_api.get_order_by_track(track)
        assert order_response.status_code == 200
        order_id = order_response.json()['order']['id']
        
        # Пытаемся принять заказ без id курьера
        response = requests.put(f'{order_api.BASE_URL}/orders/accept/{order_id}')
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.text
        
        # Очистка: отменяем заказ
        order_api.cancel_order(track)
        print("✅ Тест пройден: ошибка 400 без courierId")
    
    def test_accept_order_invalid_courier_id(self, helpers, order_api):
        """
        Тест 3: если передать неверный id курьера, запрос вернёт ошибку
        Проверяет: код 404 с сообщением "Курьера с таким id не существует"
        """
        # Создаем заказ
        order_data = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-08-09",
            "comment": "Test order",
            "color": ["BLACK"]
        }
        create_response = order_api.create_order(order_data)
        assert create_response.status_code == 201
        track = create_response.json()['track']
        
        # Получаем id заказа
        order_response = order_api.get_order_by_track(track)
        assert order_response.status_code == 200
        order_id = order_response.json()['order']['id']
        
        # Пытаемся принять заказ с несуществующим курьером
        response = order_api.accept_order(order_id, 999999)
        assert response.status_code == 404
        # Исправлено: реальное сообщение API
        assert "Курьера с таким id не существует" in response.text
        
        # Очистка: отменяем заказ
        order_api.cancel_order(track)
        print("✅ Тест пройден: ошибка 404 с неверным courierId")
    
    def test_accept_order_invalid_order_id(self, helpers, order_api):
        """
        Тест 4: если передать неверный id заказа, запрос вернёт ошибку
        Проверяет: код 404 с сообщением "Заказа с таким id не существует"
        """
        # Создаем курьера
        courier_data = helpers.register_new_courier()
        assert courier_data is not None
        courier_id = helpers.get_courier_id(courier_data['login'], courier_data['password'])
        assert courier_id is not None
        
        # Пытаемся принять несуществующий заказ
        response = order_api.accept_order(999999, courier_id)
        assert response.status_code == 404
        # Исправлено: реальное сообщение API
        assert "Заказа с таким id не существует" in response.text
        
        # Очистка: удаляем курьера
        helpers.delete_courier(courier_id)
        print("✅ Тест пройден: ошибка 404 с неверным orderId")