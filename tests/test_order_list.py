import pytest
from src.api.order_api import OrderAPI

class TestOrderList:
    """Класс для тестирования получения списка заказов"""
    
    @pytest.fixture
    def order_api(self):
        return OrderAPI()
    
    def test_get_orders_list_success(self, order_api):
        """Тест: в тело ответа возвращается список заказов"""
        response = order_api.get_orders_list()
        
        assert response.status_code == 200
        assert 'orders' in response.json()
        
        orders = response.json()['orders']
        assert isinstance(orders, list)
        
        if len(orders) > 0:
            first_order = orders[0]
            assert 'id' in first_order
            assert 'firstName' in first_order
            assert 'lastName' in first_order
            assert 'address' in first_order
            assert 'track' in first_order