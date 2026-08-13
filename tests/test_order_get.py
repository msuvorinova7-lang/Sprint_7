import allure

from src.data.order_data import OrderData


class TestOrderGet:
    """Тесты получения заказа по номеру трека."""

    @allure.title("Получение заказа по треку")
    @allure.description("Проверка получения существующего заказа по треку")
    def test_get_order_by_track_success(
            self,
            create_test_order,
            order_api
    ):
        """Проверка получения существующего заказа."""

        track = create_test_order

        response = order_api.get_order_by_track(track)

        assert response.status_code == 200

        order = response.json()

        assert order["order"]["track"] == track

    @allure.title("Получение заказа без трека")
    @allure.description("Проверка ошибки при отсутствии номера заказа")
    def test_get_order_without_track_error(self, order_api):
        """Проверка получения заказа без трека."""

        response = order_api.get_order_by_track()

        assert response.status_code == 400

    @allure.title("Получение заказа с пустым треком")
    def test_get_order_with_empty_track_error(self, order_api):
        """Проверка получения заказа с пустым треком."""

        response = order_api.get_order_by_track("")

        assert response.status_code == 400

    @allure.title("Получение заказа с несуществующим треком")
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

    @allure.title("Получение отменённого заказа")
    def test_get_order_after_cancellation(
            self,
            create_test_order,
            order_api
    ):
        """Проверка получения отменённого заказа."""

        track = create_test_order

        response = order_api.get_order_by_track(track)

        assert response.status_code == 200