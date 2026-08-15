import allure

from src.api.courier_api import CourierAPI
from src.helpers.courier_helpers import CourierHelpers


class TestCourierLogin:
    """Тесты авторизации курьера."""

    @allure.title("Успешная авторизация курьера")
    @allure.description(
        "Проверка успешной авторизации зарегистрированного курьера"
    )
    def test_login_courier_success(self, courier_helpers):
        _, courier_data, courier_id = courier_helpers

        response = CourierAPI.login_courier({
            "login": courier_data["login"],
            "password": courier_data["password"]
        })

        assert response.status_code == 200
        assert response.json()["id"] == courier_id

    @allure.title("Авторизация без логина")
    @allure.description(
        "Проверка ошибки при отсутствии обязательного поля login"
    )
    def test_login_courier_without_login(self):
        response = CourierAPI.login_courier({
            "password": CourierHelpers.generate_random_string(10)
        })

        assert response.status_code == 400
        assert "message" in response.json()

    @allure.title("Авторизация с неверным логином")
    @allure.description(
        "Проверка ошибки при указании несуществующего логина"
    )
    def test_login_courier_wrong_login(self, courier_helpers):
        _, courier_data, _ = courier_helpers

        response = CourierAPI.login_courier({
            "login": CourierHelpers.generate_random_string(10),
            "password": courier_data["password"]
        })

        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Учетная запись не найдена"
        }

    @allure.title("Авторизация с неверным паролем")
    @allure.description(
        "Проверка ошибки при указании неверного пароля"
    )
    def test_login_courier_wrong_password(self, courier_helpers):
        _, courier_data, _ = courier_helpers

        response = CourierAPI.login_courier({
            "login": courier_data["login"],
            "password": CourierHelpers.generate_random_string(10)
        })

        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Учетная запись не найдена"
        }

    @allure.title("Авторизация несуществующего курьера")
    @allure.description(
        "Проверка ошибки при авторизации несуществующего курьера"
    )
    def test_login_nonexistent_courier(self):
        response = CourierAPI.login_courier({
            "login": CourierHelpers.generate_random_string(10),
            "password": CourierHelpers.generate_random_string(10)
        })

        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Учетная запись не найдена"
        }
