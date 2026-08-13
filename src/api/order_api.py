import requests

from src.api.base_api import BaseAPI


class OrderAPI(BaseAPI):
    """Класс для работы с API заказов."""

    CREATE_ORDER_ENDPOINT = "/orders"
    GET_ORDER_ENDPOINT = "/orders/track"
    ORDERS_LIST_ENDPOINT = "/orders"
    ACCEPT_ORDER_ENDPOINT = "/orders/accept"
    CANCEL_ORDER_ENDPOINT = "/orders/cancel"

    def create_order(self, payload):
        """Создаёт новый заказ."""

        return requests.post(
            self.BASE_URL + self.CREATE_ORDER_ENDPOINT,
            json=payload
        )

    def get_order_by_track(self, track=None):
        """Получает заказ по номеру трека."""

        params = {}

        if track is not None:
            params["t"] = track

        return requests.get(
            self.BASE_URL + self.GET_ORDER_ENDPOINT,
            params=params
        )

    def get_orders_list(self):
        """Получает список заказов."""

        return requests.get(
            self.BASE_URL + self.ORDERS_LIST_ENDPOINT
        )

    def accept_order(self, track, courier_id):
        """Принимает заказ курьером."""

        # Получаем заказ по треку
        order_response = self.get_order_by_track(track)

        if order_response.status_code != 200:
            return order_response

        order_data = order_response.json()

        # В ответе API заказ находится внутри ключа "order"
        order = order_data.get("order")

        if not order:
            return order_response

        order_id = order.get("id")

        params = {}

        if courier_id is not None:
            params["courierId"] = courier_id

        return requests.put(
            f"{self.BASE_URL}{self.ACCEPT_ORDER_ENDPOINT}/{order_id}",
            params=params
        )

    def cancel_order(self, track):
        """Отменяет заказ по треку."""

        return requests.put(
            self.BASE_URL + self.CANCEL_ORDER_ENDPOINT,
            params={
                "track": track
            }
        )