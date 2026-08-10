import requests

class CourierAPI:
    """Класс для работы с API курьеров"""
    
    BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'
    
    @staticmethod
    def create_courier(data):
        """Создание курьера"""
        response = requests.post(f'{CourierAPI.BASE_URL}/courier', data=data)
        return response
    
    @staticmethod
    def login_courier(data):
        """Логин курьера"""
        response = requests.post(f'{CourierAPI.BASE_URL}/courier/login', data=data)
        return response
    
    @staticmethod
    def delete_courier(courier_id):
        """Удаление курьера"""
        response = requests.delete(f'{CourierAPI.BASE_URL}/courier/{courier_id}')
        return response