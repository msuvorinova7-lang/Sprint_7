import allure

from src.data.order_data import OrderData


class TestOrderAccept:
    """Тесты принятия заказа курьером."""

    @allure.title("Успешное принятие заказа курьером")
    @allure.description(
        "Проверка успешного принятия заказа существующим курьером"
    )
    def test_accept_order_success(
        self,
        courier_helpers,
        order_api,
        create_test_order
    ):
        _, _, courier_id = courier_helpers

        response = order_api.accept_order(
            create_test_order,
            courier_id
        )

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Принятие заказа без id курьера")
    def test_accept_order_without_courier_id(
        self,
        order_api,
        create_test_order
    ):
        response = order_api.accept_order(
            create_test_order,
            None
        )

        assert response.status_code == 400
        assert "message" in response.json()

    @allure.title("Принятие заказа с неверным id курьера")
    def test_accept_order_invalid_courier_id(
        self,
        order_api,
        create_test_order
    ):
        response = order_api.accept_order(
            create_test_order,
            999999
        )

        assert response.status_code == 404
        assert "message" in response.json()

    @allure.title("Принятие заказа без id заказа")
    def test_accept_order_without_order_id(
        self,
        order_api,
        courier_helpers
    ):
        _, _, courier_id = courier_helpers

        response = order_api.accept_order(
            None,
            courier_id
        )

        assert response.status_code == 404
        assert response.json() == {
            "code": 404,
            "message": "Not Found."
        }

    @allure.title("Принятие заказа с неверным id заказа")
    def test_accept_order_invalid_order_id(
        self,
        order_api,
        courier_helpers
    ):
        _, _, courier_id = courier_helpers

        response = order_api.accept_order(
            999999,
            courier_id
        )

        assert response.status_code == 404
        assert "message" in response.json()
