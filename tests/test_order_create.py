import allure
import pytest

from src.data.order_data import OrderData


class TestOrderCreate:
    """Тесты создания заказа."""

    @allure.title("Создание заказа с разными вариантами цвета")
    @allure.description(
        "Проверка создания заказа с BLACK, GREY, "
        "двумя цветами и без указания цвета"
    )
    @pytest.mark.parametrize(
        "order_data",
        [
            OrderData.ORDER_DATA,
            OrderData.ORDER_DATA_GREY,
            OrderData.ORDER_DATA_BOTH_COLORS,
            OrderData.ORDER_DATA_WITHOUT_COLOR
        ]
    )
    def test_create_order_with_different_colors(
        self,
        order_api,
        order_data
    ):
        response = order_api.create_order(order_data.copy())

        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
        assert response.json()["track"] > 0

        order_api.cancel_order(response.json()["track"])
