import allure

from src.data.order_data import OrderData


class TestOrderGet:
    """Тесты получения заказа по номеру трека."""

    @allure.title("Получение заказа по треку")
    def test_get_order_by_track_success(self, order_api):
        """Проверка получения заказа по номеру трека."""

        order_data = OrderData.ORDER_DATA.copy()

        create_response = order_api.create_order(order_data)

        assert create_response.status_code == 201

        track = create_response.json()["track"]

        response = order_api.get_order_by_track(track)

        assert response.status_code == 200
        assert response.json()["order"]["track"] == track

    @allure.title("Получение заказа без номера трека")
    def test_get_order_without_track_error(self, order_api):
        """Проверка получения заказа без номера трека."""

        response = order_api.get_order_by_track(None)

        assert response.status_code == 400

    @allure.title("Получение заказа с пустым номером трека")
    def test_get_order_with_empty_track_error(self, order_api):
        """Проверка получения заказа с пустым номером трека."""

        response = order_api.get_order_by_track("")

        assert response.status_code == 400

    @allure.title("Получение несуществующего заказа")
    def test_get_order_nonexistent_track_error(self, order_api):
        """Проверка получения заказа с несуществующим треком."""

        response = order_api.get_order_by_track(999999999)

        assert response.status_code == 404

    @allure.title("Получение заказа с отрицательным треком")
    def test_get_order_with_negative_track_error(self, order_api):
        """Проверка получения заказа с отрицательным номером трека."""

        response = order_api.get_order_by_track(-1)

        assert response.status_code == 500

    @allure.title("Получение заказа со строковым треком")
    def test_get_order_with_string_track_error(self, order_api):
        """Проверка получения заказа со строковым номером трека."""

        response = order_api.get_order_by_track("abc")

        assert response.status_code == 500

    @allure.title("Получение отмененного заказа")
    def test_get_order_after_cancellation(self, order_api):
        """Проверка получения заказа после отмены."""

        order_data = OrderData.ORDER_DATA.copy()

        create_response = order_api.create_order(order_data)

        assert create_response.status_code == 201

        track = create_response.json()["track"]

        cancel_response = order_api.cancel_order(track)

        assert cancel_response.status_code == 200

        response = order_api.get_order_by_track(track)

        assert response.status_code == 404