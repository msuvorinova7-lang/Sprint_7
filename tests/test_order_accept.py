import allure
import pytest
import requests
from src.helpers.courier_helpers import CourierHelpers
from src.api.order_api import OrderAPI
from src.data.order_data import OrderData

class TestOrderAccept:
    """Класс для тестирования принятия заказа (ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ)"""
    
    @pytest.fixture
    def helpers(self):
        return CourierHelpers()
    
    @pytest.fixture
    def order_api(self):
        return OrderAPI()
    
    @allure.title("Успешное принятие заказа")
    @allure.description("Проверка, что заказ успешно принимается курьером")
    def test_accept_order_success(self, helpers, order_api):
        """Тест: успешное принятие заказа"""
        # Создаем курьера
        courier_data = helpers.register_new_courier()
        assert courier_data is not None
        courier_id = helpers.get_courier_id(courier_data['login'], courier_data['password'])
        assert courier_id is not None
        
        # Создаем заказ
        order_data = OrderData.get_order_data()
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
        
        # Очистка: удаляем курьера (заказ нельзя отменить после принятия)
        helpers.delete_courier(courier_id)
    
    @allure.title("Принятие заказа без id курьера")
    @allure.description("Проверка ошибки при отсутствии id курьера")
    def test_accept_order_without_courier_id(self, helpers, order_api):
        """Тест: если не передать id курьера, запрос вернёт ошибку"""
        # Создаем заказ
        order_data = OrderData.get_order_data()
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
    
    @allure.title("Принятие заказа с неверным id курьера")
    @allure.description("Проверка ошибки при передаче несуществующего id курьера")
    def test_accept_order_invalid_courier_id(self, helpers, order_api):
        """Тест: если передать неверный id курьера, запрос вернёт ошибку"""
        # Создаем заказ
        order_data = OrderData.get_order_data()
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
        assert "Курьера с таким id не существует" in response.text
        
        # Очистка: отменяем заказ
        order_api.cancel_order(track)
    
    @allure.title("Принятие заказа с неверным id заказа")
    @allure.description("Проверка ошибки при передаче несуществующего id заказа")
    def test_accept_order_invalid_order_id(self, helpers, order_api):
        """Тест: если передать неверный id заказа, запрос вернёт ошибку"""
        # Создаем курьера
        courier_data = helpers.register_new_courier()
        assert courier_data is not None
        courier_id = helpers.get_courier_id(courier_data['login'], courier_data['password'])
        assert courier_id is not None
        
        # Пытаемся принять несуществующий заказ
        response = order_api.accept_order(999999, courier_id)
        assert response.status_code == 404
        assert "Заказа с таким id не существует" in response.text
        
        # Очистка: удаляем курьера
        helpers.delete_courier(courier_id)