import allure
import pytest
import requests

from src.helpers.courier_helpers import CourierHelpers
from src.api.courier_api import CourierAPI


class TestCourierDelete:
    """Класс для тестирования удаления курьера"""

    @pytest.fixture
    def helpers(self):
        return CourierHelpers()

    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self, helpers):
        """Тест: успешное удаление курьера"""
        courier_data = helpers.register_new_courier()

        courier_id = helpers.get_courier_id(
            courier_data['login'],
            courier_data['password']
        )

        response = helpers.delete_courier(courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Удаление курьера с несуществующим id")
    def test_delete_courier_invalid_id_error(self, helpers):
        """Тест: ошибка при удалении с несуществующим id"""
        response = helpers.delete_courier(999999)

        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Курьера с таким id нет."
        }

    @allure.title("Удаление курьера без id")
    def test_delete_courier_without_id_error(self, helpers):
        """Тест: ошибка при удалении без id"""
        response = requests.delete(
            f'{CourierAPI.BASE_URL}/courier/'
        )

        assert response.status_code == 404