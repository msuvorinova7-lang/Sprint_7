import allure
import requests
from src.api.base_api import BaseAPI

class OrderAPI(BaseAPI):
    """Класс для работы с API заказов"""
    
    @staticmethod
    @allure.step("Создание заказа")
    def create_order(order_data):
        """Создание заказа"""
        response = requests.post(f'{BaseAPI.BASE_URL}/orders', json=order_data)
        return response
    
    @staticmethod
    @allure.step("Получение списка заказов")
    def get_orders_list():
        """Получение списка заказов"""
        response = requests.get(f'{BaseAPI.BASE_URL}/orders')
        return response
    
    @staticmethod
    @allure.step("Отмена заказа по треку {track}")
    def cancel_order(track):
        """Отмена заказа"""
        response = requests.put(f'{BaseAPI.BASE_URL}/orders/cancel', params={'track': track})
        return response
    
    @staticmethod
    @allure.step("Принятие заказа {order_id} курьером {courier_id}")
    def accept_order(order_id, courier_id):
        """Принятие заказа"""
        response = requests.put(f'{BaseAPI.BASE_URL}/orders/accept/{order_id}', 
                              params={'courierId': courier_id})
        return response
    
    @staticmethod
    @allure.step("Получение заказа по треку {track}")
    def get_order_by_track(track):
        """Получение заказа по треку"""
        response = requests.get(f'{BaseAPI.BASE_URL}/orders/track', 
                              params={'t': track})
        return response