import random
import string

from src.api.courier_api import CourierAPI


class CourierHelpers:
    """Вспомогательные методы для работы с курьером."""

    @staticmethod
    def generate_random_string(length):
        """Генерирует случайную строку."""
        letters = string.ascii_lowercase
        return ''.join(
            random.choice(letters)
            for _ in range(length)
        )

    def create_courier(self, courier_data):
        """Создаёт курьера."""
        return CourierAPI.create_courier(courier_data)

    def register_new_courier(self):
        """Создаёт нового уникального курьера."""

        courier_data = {
            "login": self.generate_random_string(10),
            "password": self.generate_random_string(10),
            "firstName": self.generate_random_string(10)
        }

        response = self.create_courier(courier_data)

        if response.status_code != 201:
            return None

        return {
            "login": courier_data["login"],
            "password": courier_data["password"],
            "first_name": courier_data["firstName"]
        }

    def get_courier_id(self, login, password):
        """Получает id курьера."""

        response = CourierAPI.login_courier({
            "login": login,
            "password": password
        })

        if response.status_code != 200:
            raise RuntimeError("Не удалось получить id курьера")

        return response.json()["id"]

    def login_courier(self, login, password):
        """Авторизует курьера."""

        return CourierAPI.login_courier({
            "login": login,
            "password": password
        })

    def delete_courier(self, courier_id):
        """Удаляет курьера."""
        return CourierAPI.delete_courier(courier_id)
