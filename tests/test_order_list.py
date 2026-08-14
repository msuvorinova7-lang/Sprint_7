import allure


class TestOrderList:
    """Тесты получения списка заказов."""

    @allure.title("Получение списка заказов")
    @allure.description(
        "Проверка получения списка заказов"
    )
    def test_get_orders_list_success(self, order_api):
        """Проверяет успешное получение списка заказов."""

        response = order_api.get_orders_list()

        orders = response.json()["orders"]

        assert (
            response.status_code == 200
            and isinstance(orders, list)
        )
