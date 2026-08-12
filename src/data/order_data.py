class OrderData:
    @staticmethod
    def get_order_data(color=None):
        data = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-08-12",
            "comment": "Saske, come back to Konoha",
            "color": color if color is not None else ["BLACK"]
        }
        return data