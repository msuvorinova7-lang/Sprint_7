import allure


class TestOrderGet:
    """Тесты получения заказа по номеру трека."""

    @allure.title("Получение заказа по треку")
    @allure.description(
        "Проверка получения существующего заказа по треку"
    )
    def test_get_order_by_track_success(
        self,
        create_test_order,
        order_api
    ):
        response = order_api.get_order_by_track(
            create_test_order
        )

        assert response.status_code == 200
        assert "order" in response.json()
        assert response.json()["order"]["track"] == create_test_order

    @allure.title("Получение заказа без номера")
    def test_get_order_without_track_error(self, order_api):
        response = order_api.get_order_by_track()

        assert response.status_code == 400
        assert "message" in response.json()

    @allure.title("Получение несуществующего заказа")
    def test_get_order_nonexistent_track_error(self, order_api):
        response = order_api.get_order_by_track(999999999)

        assert response.status_code == 404
        assert "message" in response.json()
