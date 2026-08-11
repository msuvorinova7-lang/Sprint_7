import allure
import requests
from src.api.base_api import BaseAPI

class CourierAPI(BaseAPI):
    """Класс для работы с API курьеров"""
    
    @staticmethod
    @allure.step("Создание курьера")
    def create_courier(data):
        """Создание курьера"""
        response = requests.post(f'{BaseAPI.BASE_URL}/courier', data=data)
        return response
    
    @staticmethod
    @allure.step("Логин курьера")
    def login_courier(data):
        """Логин курьера"""
        response = requests.post(f'{BaseAPI.BASE_URL}/courier/login', data=data)
        return response
    
    @staticmethod
    @allure.step("Удаление курьера по id {courier_id}")
    def delete_courier(courier_id):
        """Удаление курьера"""
        response = requests.delete(f'{BaseAPI.BASE_URL}/courier/{courier_id}')
        return response