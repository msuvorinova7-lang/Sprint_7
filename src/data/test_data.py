class TestData:
    """Класс с тестовыми данными"""
    
    # Данные для создания заказа
    ORDER_DATA = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2026-08-07",
        "comment": "Saske, come back to Konoha",
        "color": ["BLACK"]
    }
    
    # Данные для создания курьера
    COURIER_DATA = {
        "login": "test_courier",
        "password": "test_password",
        "firstName": "Test"
    }
    
    # Невалидные данные
    INVALID_LOGIN = "invalid_login"
    INVALID_PASSWORD = "invalid_password"
    INVALID_ID = 999999