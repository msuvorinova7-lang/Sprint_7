import allure
import pytest
from src.helpers.courier_helpers import CourierHelpers
from src.api.courier_api import CourierAPI

class TestCourierCreate:
    """Класс для тестирования создания курьера"""
    
    @pytest.fixture
    def helpers(self):
        return CourierHelpers()
    
    @allure.title("Успешное создание курьера")
    @allure.description("Проверка, что курьера можно создать с валидными данными")
    def test_create_courier_success(self, helpers):
        """Тест: можно создать курьера"""
        courier_data = helpers.register_new_courier()
        assert courier_data is not None, "Курьер не был создан"
        
        response = helpers.login_courier(courier_data['login'], courier_data['password'])
        assert response.status_code == 200, "Не удалось авторизоваться"
        assert 'id' in response.json(), "В ответе нет id курьера"
        
        courier_id = response.json()['id']
        delete_response = helpers.delete_courier(courier_id)
        assert delete_response.status_code == 200, "Не удалось удалить курьера"
    
    @allure.title("Создание дубликата курьера")
    @allure.description("Проверка, что нельзя создать двух курьеров с одинаковым логином")
    def test_create_duplicate_courier_error(self, helpers):
        """Тест: нельзя создать двух одинаковых курьеров"""
        courier_data = helpers.register_new_courier()
        assert courier_data is not None
        
        payload = {
            "login": courier_data['login'],
            "password": courier_data['password'],
            "firstName": courier_data['first_name']
        }
        response = CourierAPI.create_courier(payload)
        
        assert response.status_code == 409
        assert response.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}
        
        courier_id = helpers.get_courier_id(courier_data['login'], courier_data['password'])
        if courier_id:
            helpers.delete_courier(courier_id)
    
    @allure.title("Создание курьера без обязательных полей")
    @allure.description("Проверка ошибки при отсутствии логина или пароля")
    def test_create_courier_missing_fields(self, helpers):
        """Тест: запрос возвращает ошибку, если одного из полей нет"""
        # Без логина
        payload = {
            "password": helpers.generate_random_string(10),
            "firstName": helpers.generate_random_string(10)
        }
        response = CourierAPI.create_courier(payload)
        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.text
    
    @allure.title("Проверка формата успешного ответа")
    @allure.description("Успешный запрос должен возвращать {'ok': true}")
    def test_create_courier_success_response(self, helpers):
        """Тест: успешный запрос возвращает {"ok":true}"""
        payload = {
            "login": helpers.generate_random_string(10),
            "password": helpers.generate_random_string(10),
            "firstName": helpers.generate_random_string(10)
        }
        response = CourierAPI.create_courier(payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
        
        courier_id = helpers.get_courier_id(payload['login'], payload['password'])
        if courier_id:
            helpers.delete_courier(courier_id)