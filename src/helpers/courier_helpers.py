import requests
import random
import string
from src.api.courier_api import CourierAPI

class CourierHelpers:
    """Вспомогательный класс для работы с курьерами"""
    
    @staticmethod
    def generate_random_string(length=10):
        """Генерирует случайную строку из букв нижнего регистра"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
    def register_new_courier(self):
        """Регистрирует нового курьера с случайными данными"""
        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = CourierAPI.create_courier(payload)
        
        if response.status_code == 201:
            return {
                "login": login,
                "password": password,
                "first_name": first_name,
                "id": None
            }
        return None
    
    def login_courier(self, login, password):
        """Авторизует курьера"""
        payload = {
            "login": login,
            "password": password
        }
        return CourierAPI.login_courier(payload)
    
    def delete_courier(self, courier_id):
        """Удаляет курьера"""
        return CourierAPI.delete_courier(courier_id)
    
    def get_courier_id(self, login, password):
        """Получает id курьера"""
        response = self.login_courier(login, password)
        if response.status_code == 200:
            return response.json().get('id')
        return None
