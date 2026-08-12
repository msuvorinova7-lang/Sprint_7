import allure
import pytest

from src.helpers.courier_helpers import CourierHelpers
from src.api.courier_api import CourierAPI


class TestCourierLogin:
    """Тесты авторизации курьера"""

    @pytest.fixture
    def helpers(self):
        return CourierHelpers()

    @allure.title("Успешная авторизация курьера")
    def test_login_courier_success(self, helpers):
        """Проверка успешной авторизации курьера"""
        courier_data = helpers.register_new_courier()

        response = helpers.login_courier(
            courier_data['login'],
            courier_data['password']
        )

        assert response.status_code == 200

        courier_id = response.json()['id']

        helpers.delete_courier(courier_id)

    @allure.title("Авторизация без логина")
    def test_login_courier_without_login(self, helpers):
        """Проверка авторизации без логина"""
        payload = {
            "password": helpers.generate_random_string(10)
        }

        response = CourierAPI.login_courier(payload)

        assert response.status_code == 400

    @allure.title("Авторизация без пароля")
    def test_login_courier_without_password(self, helpers):
        """Проверка авторизации без пароля"""
        payload = {
            "login": helpers.generate_random_string(10)
        }

        response = CourierAPI.login_courier(payload)

        assert response.status_code == 504

    @allure.title("Авторизация с пустыми данными")
    def test_login_courier_empty_data(self, helpers):
        """Проверка авторизации с пустым запросом"""
        response = CourierAPI.login_courier({})

        assert response.status_code == 504

    @allure.title("Авторизация с неверным логином")
    def test_login_courier_wrong_login(self, helpers):
        """Проверка авторизации с неверным логином"""
        courier_data = helpers.register_new_courier()

        response = helpers.login_courier(
            helpers.generate_random_string(10),
            courier_data['password']
        )

        assert response.status_code == 404

        courier_id = helpers.get_courier_id(
            courier_data['login'],
            courier_data['password']
        )

        helpers.delete_courier(courier_id)

    @allure.title("Авторизация с неверным паролем")
    def test_login_courier_wrong_password(self, helpers):
        """Проверка авторизации с неверным паролем"""
        courier_data = helpers.register_new_courier()

        response = helpers.login_courier(
            courier_data['login'],
            helpers.generate_random_string(10)
        )

        assert response.status_code == 404

        courier_id = helpers.get_courier_id(
            courier_data['login'],
            courier_data['password']
        )

        helpers.delete_courier(courier_id)

    @allure.title("Авторизация несуществующего курьера")
    def test_login_nonexistent_courier(self, helpers):
        """Проверка авторизации несуществующего курьера"""
        response = helpers.login_courier(
            helpers.generate_random_string(10),
            helpers.generate_random_string(10)
        )

        assert response.status_code == 404