class OrderData:
    """Тестовые данные для заказов."""

    ORDER_DATA = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "Москва, ул. Тверская, 1",
        "metroStation": 1,
        "phone": "+7 800 555-35-35",
        "rentTime": 2,
        "deliveryDate": "2026-08-20",
        "comment": "Позвонить за час",
        "color": ["BLACK"]
    }

    ORDER_DATA_GREY = {
        **ORDER_DATA,
        "color": ["GREY"]
    }

    ORDER_DATA_BOTH_COLORS = {
        **ORDER_DATA,
        "color": ["BLACK", "GREY"]
    }

    ORDER_DATA_WITHOUT_COLOR = {
        key: value
        for key, value in ORDER_DATA.items()
        if key != "color"
    }
