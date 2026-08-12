import pytest
from src.helpers.courier_helpers import CourierHelpers

@pytest.fixture
def courier_helpers():
    """Фикстура для работы с курьерами"""
    return CourierHelpers()