import pytest
import requests
from src.helpers.courier_helpers import CourierHelpers

@pytest.fixture
def courier_helpers():
    """Фикстура для работы с курьерами"""
    return CourierHelpers()

@pytest.fixture
def base_url():
    """Базовый URL API"""
    return 'https://qa-scooter.praktikum-services.ru/api/v1'

@pytest.fixture
def delete_courier_after_test():
    """Фикстура для удаления курьера после теста"""
    courier_id = None
    
    def _set_courier_id(courier_id_value):
        nonlocal courier_id
        courier_id = courier_id_value
    
    yield _set_courier_id
    
    if courier_id:
        response = requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
        if response.status_code == 200:
            print(f"Курьер с id {courier_id} удален")