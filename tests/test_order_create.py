import pytest
from src.api.order_api import OrderAPI

class TestOrderCreate:
    """Класс для тестирования создания заказа"""
    
    @pytest.fixture
    def order_api(self):
        return OrderAPI()
    
    @pytest.mark.parametrize('color', [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, order_api, color):
        """Тест: создание заказа с разными цветами"""
        order_data = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-08-07",
            "comment": "Saske, come back to Konoha",
            "color": color
        }
        
        response = order_api.create_order(order_data)
        
        assert response.status_code == 201
        assert 'track' in response.json()
        assert isinstance(response.json()['track'], int)
        assert response.json()['track'] > 0
        
        track = response.json()['track']
        order_api.cancel_order(track)