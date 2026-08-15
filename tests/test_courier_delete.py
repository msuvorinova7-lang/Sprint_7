import allure

from src.api.courier_api import CourierAPI


class TestCourierDelete:
    """Тесты удаления курьера."""

    @allure.title("Успешное удаление курьера")
    @allure.description(
        "Проверка успешного удаления существующего курьера"
    )
    def test_delete_courier_success(self, courier_helpers):
        _, _, courier_id = courier_helpers

        response = CourierAPI.delete_courier(courier_id)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Удаление курьера с несуществующим id")
    def test_delete_courier_invalid_id(self):
        response = CourierAPI.delete_courier(999999)

        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Курьера с таким id нет."
        }

    @allure.title("Удаление курьера без id")
    def test_delete_courier_without_id(self):
        response = CourierAPI.delete_courier(None)

        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Not Found."
        }
