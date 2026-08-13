import allure

from src.data.order_data import OrderData


class TestOrderAccept:
    """Тесты принятия заказа курьером."""

    @allure.title("Успешное принятие заказа курьером")
    @allure.description("Проверка успешного принятия заказа курьером")
    def test_accept_order_success(self, courier_helpers, order_api):
        """Проверка успешного принятия заказа."""

        helpers, courier_data = courier_helpers

        courier_id = helpers.get_courier_id(
            courier_data["login"],
            courier_data["password"]
        )

        create_response = order_api.create_order(
            OrderData.ORDER_DATA.copy()
        )

        assert create_response.status_code == 201

        order_track = create_response.json()["track"]

        response = order_api.accept_order(
            order_track,
            courier_id
        )

        assert response.status_code == 200

    @allure.title("Принятие заказа без id курьера")
    @allure.description("Проверка ошибки при отсутствии courierId")
    def test_accept_order_without_courier_id(self, order_api):
        """Проверка принятия заказа без id курьера."""

        create_response = order_api.create_order(
            OrderData.ORDER_DATA.copy()
        )

        assert create_response.status_code == 201

        order_track = create_response.json()["track"]

        response = order_api.accept_order(
            order_track,
            None
        )

        assert response.status_code == 400

    @allure.title("Принятие заказа с неверным id курьера")
    @allure.description("Проверка ошибки с несуществующим courierId")
    def test_accept_order_invalid_courier_id(self, order_api):
        """Проверка принятия заказа с несуществующим id курьера."""

        create_response = order_api.create_order(
            OrderData.ORDER_DATA.copy()
        )

        assert create_response.status_code == 201

        order_track = create_response.json()["track"]

        response = order_api.accept_order(
            order_track,
            999999
        )

        assert response.status_code == 404

    @allure.title("Принятие заказа с неверным id заказа")
    @allure.description("Проверка ошибки с несуществующим номером заказа")
    def test_accept_order_invalid_order_id(self, order_api):
        """Проверка принятия несуществующего заказа."""

        response = order_api.accept_order(
            999999,
            999999
        )

        assert response.status_code == 404