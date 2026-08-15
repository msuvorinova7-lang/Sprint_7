import allure
import requests

from src.api.base_api import BaseAPI


class OrderAPI(BaseAPI):
    """Класс для работы с API заказов."""

    CREATE_ORDER_ENDPOINT = "/orders"
    GET_ORDER_ENDPOINT = "/orders/track"
    ORDERS_LIST_ENDPOINT = "/orders"
    ACCEPT_ORDER_ENDPOINT = "/orders/accept"
    CANCEL_ORDER_ENDPOINT = "/orders/cancel"

    @allure.step("Создание заказа")
    def create_order(self, payload):
        """Создаёт новый заказ."""
        return requests.post(
            f"{self.BASE_URL}{self.CREATE_ORDER_ENDPOINT}",
            json=payload
        )

    @allure.step("Получение заказа по номеру трека")
    def get_order_by_track(self, track=None):
        """Получает заказ по номеру трека."""

        params = {}

        if track is not None:
            params["t"] = track

        return requests.get(
            f"{self.BASE_URL}{self.GET_ORDER_ENDPOINT}",
            params=params
        )

    @allure.step("Получение списка заказов")
    def get_orders_list(self):
        """Получает список заказов."""
        return requests.get(
            f"{self.BASE_URL}{self.ORDERS_LIST_ENDPOINT}"
        )

    @allure.step("Принятие заказа курьером")
    def accept_order(self, track, courier_id):
        """Принимает заказ курьером."""

        if track is None:
            return requests.put(
                f"{self.BASE_URL}{self.ACCEPT_ORDER_ENDPOINT}/",
                params={"courierId": courier_id}
            )

        order_response = self.get_order_by_track(track)

        if order_response.status_code != 200:
            return order_response

        order_id = order_response.json()["order"]["id"]

        params = {}

        if courier_id is not None:
            params["courierId"] = courier_id

        return requests.put(
            f"{self.BASE_URL}{self.ACCEPT_ORDER_ENDPOINT}/{order_id}",
            params=params
        )

    @allure.step("Отмена заказа по номеру трека")
    def cancel_order(self, track):
        """Отменяет заказ по треку."""
        return requests.put(
            f"{self.BASE_URL}{self.CANCEL_ORDER_ENDPOINT}",
            params={"track": track}
        )
