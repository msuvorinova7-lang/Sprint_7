import requests

class OrderAPI:
    """Класс для работы с API заказов"""
    
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'
    
    @staticmethod
    def create_order(order_data):
        """Создание заказа"""
        response = requests.post(f'{OrderAPI.BASE_URL}/orders', json=order_data)
        return response
    
    @staticmethod
    def get_orders_list():
        """Получение списка заказов"""
        response = requests.get(f'{OrderAPI.BASE_URL}/orders')
        return response
    
    @staticmethod
    def cancel_order(track):
        """Отмена заказа"""
        response = requests.put(f'{OrderAPI.BASE_URL}/orders/cancel', params={'track': track})
        return response
    
    @staticmethod
    def accept_order(order_id, courier_id):
        """Принятие заказа"""
        response = requests.put(f'{OrderAPI.BASE_URL}/orders/accept/{order_id}', 
                              params={'courierId': courier_id})
        return response
    
    @staticmethod
    def get_order_by_track(track):
        """Получение заказа по треку"""
        response = requests.get(f'{OrderAPI.BASE_URL}/orders/track', 
                              params={'t': track})
        return response