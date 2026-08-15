import allure


class TestOrderList:
    """Тесты получения списка заказов."""

    @allure.title("Получение списка заказов")
    @allure.description(
        "Проверка получения списка заказов"
    )
    def test_get_orders_list_success(
        self,
        order_api,
        create_test_order
    ):
        response = order_api.get_orders_list()

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
