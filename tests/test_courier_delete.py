import pytest
import requests
from src.helpers.courier_helpers import CourierHelpers
from src.api.courier_api import CourierAPI

class TestCourierDelete:
    """Класс для тестирования удаления курьера"""
    
    @pytest.fixture
    def helpers(self):
        return CourierHelpers()
    
    def test_delete_courier_success(self, helpers):
        """Тест: успешное удаление курьера"""
        courier_data = helpers.register_new_courier()
        assert courier_data is not None
        
        courier_id = helpers.get_courier_id(courier_data['login'], courier_data['password'])
        assert courier_id is not None
        
        response = helpers.delete_courier(courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}
    
    def test_delete_courier_invalid_id_error(self, helpers):
        """Тест: ошибка при удалении с несуществующим id"""
        response = helpers.delete_courier(999999)
        assert response.status_code == 404
        # Исправлено: реальное сообщение API
        assert response.json() == {"code": 404, "message": "Курьера с таким id нет."}
    
    def test_delete_courier_without_id_error(self, helpers):
        """Тест: ошибка при удалении без id"""
        response = requests.delete(f'{CourierAPI.BASE_URL}/courier/')
        assert response.status_code in [400, 404]