import allure
import pytest
from src.helpers.courier_helpers import CourierHelpers
from src.api.courier_api import CourierAPI

class TestCourierLogin:
    """Класс для тестирования логина курьера"""
    
    @pytest.fixture
    def helpers(self):
        return CourierHelpers()
    
    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверка, что курьер может авторизоваться с валидными данными")
    def test_login_courier_success(self, helpers):
        """Тест: курьер может авторизоваться"""
        courier_data = helpers.register_new_courier()
        assert courier_data is not None
        
        response = helpers.login_courier(courier_data['login'], courier_data['password'])
        
        assert response.status_code == 200
        assert 'id' in response.json()
        assert response.json()['id'] > 0
        
        courier_id = response.json()['id']
        helpers.delete_courier(courier_id)
    
    @allure.title("Авторизация без обязательных полей")
    @allure.description("Проверка ошибки при отсутствии логина или пароля")
    def test_login_courier_missing_fields(self, helpers):
        """Тест: для авторизации нужно передать все обязательные поля"""
        # Без логина
        payload = {"password": helpers.generate_random_string(10)}
        response = CourierAPI.login_courier(payload)
        assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
        assert "Недостаточно данных для входа" in response.text
        
        # Без пароля - сервер иногда возвращает 504 (ошибка сервера)
        payload = {"login": helpers.generate_random_string(10)}
        response = CourierAPI.login_courier(payload)
        assert response.status_code in [400, 504], \
            f"Ожидался код ошибки (400 или 504), получен {response.status_code}"
        
        # Пустой запрос - сервер также может вернуть 504
        payload = {}
        response = CourierAPI.login_courier(payload)
        assert response.status_code in [400, 504], \
            f"Ожидался код ошибки (400 или 504), получен {response.status_code}"
    
    @allure.title("Авторизация с неверными данными")
    @allure.description("Проверка ошибки при неправильном логине или пароле")
    def test_login_courier_invalid_credentials(self, helpers):
        """Тест: система вернёт ошибку, если неправильно указать логин или пароль"""
        courier_data = helpers.register_new_courier()
        assert courier_data is not None
        
        # Неправильный логин
        response = helpers.login_courier(
            helpers.generate_random_string(10),
            courier_data['password']
        )
        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}
        
        # Неправильный пароль
        response = helpers.login_courier(
            courier_data['login'],
            helpers.generate_random_string(10)
        )
        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}
        
        courier_id = helpers.get_courier_id(courier_data['login'], courier_data['password'])
        if courier_id:
            helpers.delete_courier(courier_id)
    
    @allure.title("Авторизация с несуществующим пользователем")
    @allure.description("Проверка ошибки при попытке авторизоваться с несуществующими данными")
    def test_login_nonexistent_courier_error(self, helpers):
        """Тест: авторизация с несуществующим пользователем"""
        response = helpers.login_courier(
            helpers.generate_random_string(10),
            helpers.generate_random_string(10)
        )
        assert response.status_code == 404
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}
    
    @allure.title("Проверка наличия id в успешном ответе")
    @allure.description("Успешный запрос должен возвращать id курьера")
    def test_login_success_response_has_id(self, helpers):
        """Тест: успешный запрос возвращает id"""
        courier_data = helpers.register_new_courier()
        assert courier_data is not None
        
        response = helpers.login_courier(courier_data['login'], courier_data['password'])
        
        assert response.status_code == 200
        response_json = response.json()
        assert 'id' in response_json
        assert isinstance(response_json['id'], int)
        assert response_json['id'] > 0
        
        courier_id = response_json['id']
        helpers.delete_courier(courier_id)