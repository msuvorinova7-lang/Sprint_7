import allure

from src.api.courier_api import CourierAPI
from src.helpers.courier_helpers import CourierHelpers


class TestCourierCreate:
    """Тесты создания курьера."""

    @allure.title("Успешное создание курьера")
    @allure.description(
        "Проверка создания курьера с валидными данными"
    )
    def test_create_courier_success(self):
        helpers = CourierHelpers()

        courier_data = {
            "login": helpers.generate_random_string(10),
            "password": helpers.generate_random_string(10),
            "firstName": helpers.generate_random_string(10)
        }

        response = CourierAPI.create_courier(courier_data)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        courier_id = helpers.get_courier_id(
            courier_data["login"],
            courier_data["password"]
        )
        helpers.delete_courier(courier_id)

    @allure.title("Создание дубликата курьера")
    @allure.description(
        "Проверка невозможности создать двух курьеров "
        "с одинаковым логином"
    )
    def test_create_duplicate_courier_error(self, courier_helpers):
        _, courier_data, _ = courier_helpers

        payload = {
            "login": courier_data["login"],
            "password": CourierHelpers.generate_random_string(10),
            "firstName": CourierHelpers.generate_random_string(10)
        }

        response = CourierAPI.create_courier(payload)

        assert response.status_code == 409
        assert response.json() == {
            "code": 409,
            "message": "Этот логин уже используется. Попробуйте другой."
        }

    @allure.title("Создание курьера без логина")
    def test_create_courier_without_login(self):
        payload = {
            "password": CourierHelpers.generate_random_string(10),
            "firstName": CourierHelpers.generate_random_string(10)
        }

        response = CourierAPI.create_courier(payload)

        assert response.status_code == 400
        assert "message" in response.json()

    @allure.title("Создание курьера без пароля")
    def test_create_courier_without_password(self):
        payload = {
            "login": CourierHelpers.generate_random_string(10),
            "firstName": CourierHelpers.generate_random_string(10)
        }

        response = CourierAPI.create_courier(payload)

        assert response.status_code == 400
        assert "message" in response.json()
