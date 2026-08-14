import allure


class TestOrderList:
    """Тесты получения списка заказов."""

    @allure.title("Получение списка заказов")
    @allure.description(
        "Проверка получения списка заказов "
        "при наличии созданного заказа"
    )
    def test_get_orders_list_success(
        self,
        order_api,
        create_test_order
    ):
        """Проверяет получение списка заказов."""

        response = order_api.get_orders_list()

        orders = response.json()["orders"]

        assert response.status_code == 200
        assert isinstance(orders, list)
