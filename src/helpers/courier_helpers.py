import random
import string

from src.api.courier_api import CourierAPI


class CourierHelpers:
    """Вспомогательные методы для работы с курьерами."""

    @staticmethod
    def generate_random_string(length=10):
        """Генерация случайной строки."""
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(length))

    def register_new_courier(self):
        """Создание нового курьера."""

        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = CourierAPI.create_courier(payload)

        assert response.status_code == 201

        return {
            "login": login,
            "password": password,
            "first_name": first_name
        }

    def login_courier(self, login, password):
        """Авторизация курьера."""

        payload = {
            "login": login,
            "password": password
        }

        return CourierAPI.login_courier(payload)

    def get_courier_id(self, login, password):
        """Получение ID курьера."""

        response = self.login_courier(login, password)

        if response.status_code == 200:
            return response.json()["id"]

        return None

    def delete_courier(self, courier_id):
        """Удаление курьера."""

        return CourierAPI.delete_courier(courier_id)