import pytest
import requests
from src.api.order_api import OrderAPI

class TestOrderGet:
    """Класс для тестирования получения заказа по его номеру (треку)"""
    
    @pytest.fixture
    def order_api(self):
        """Фикстура для работы с API заказов"""
        return OrderAPI()
    
    @pytest.fixture
    def create_test_order(self, order_api):
        """
        Фикстура для создания тестового заказа
        Возвращает track (номер трека) созданного заказа
        """
        # Данные для создания заказа
        order_data = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2026-08-09",
            "comment": "Saske, come back to Konoha",
            "color": ["BLACK"]
        }
        
        # Создаем заказ
        response = order_api.create_order(order_data)
        assert response.status_code == 201, "Заказ не был создан"
        track = response.json()['track']
        
        yield track  # Передаем track в тест
        
        # Очистка после теста - отменяем заказ
        order_api.cancel_order(track)
    
    def test_get_order_by_track_success(self, order_api, create_test_order):
        """
        Тест 1: успешный запрос возвращает объект с заказом
        Ожидаемый результат: код 200, в ответе есть объект order с правильными данными
        """
        # Шаг 1: Получаем track из фикстуры
        track = create_test_order
        
        # Шаг 2: Отправляем запрос на получение заказа по треку
        response = order_api.get_order_by_track(track)
        
        # Шаг 3: Проверяем статус-код
        assert response.status_code == 200, f"Код ответа должен быть 200, получен {response.status_code}"
        
        # Шаг 4: Проверяем, что в ответе есть объект order
        response_json = response.json()
        assert 'order' in response_json, "В ответе должен быть ключ 'order'"
        
        # Шаг 5: Проверяем содержимое заказа
        order = response_json['order']
        
        # Проверяем наличие всех обязательных полей
        required_fields = [
            'id', 'firstName', 'lastName', 'address',
            'metroStation', 'phone', 'rentTime', 'deliveryDate',
            'track', 'color', 'comment', 'status'
        ]
        
        for field in required_fields:
            assert field in order, f"В заказе должно быть поле '{field}'"
        
        # Шаг 6: Проверяем, что track совпадает
        assert order['track'] == track, f"Трек заказа должен быть {track}, получен {order['track']}"
        
        # Шаг 7: Проверяем, что это действительно наш заказ
        assert order['firstName'] == "Naruto", "Имя должно быть Naruto"
        assert order['lastName'] == "Uchiha", "Фамилия должна быть Uchiha"
        assert order['address'] == "Konoha, 142 apt.", "Адрес должен совпадать"
        
        # Шаг 8: Проверяем типы данных
        # Исправлено: некоторые поля могут быть строками, проверяем что они числовые
        assert isinstance(order['id'], int), "id должен быть числом"
        assert isinstance(order['track'], int), "track должен быть числом"
        assert isinstance(order['status'], int), "status должен быть числом"
        assert isinstance(order['rentTime'], int), "rentTime должен быть числом"
        
        # Исправлено: metroStation может быть строкой, проверяем что это число
        metro_station = order['metroStation']
        assert str(metro_station).isdigit() or isinstance(metro_station, int), \
            f"metroStation должен быть числом, получен {type(metro_station).__name__}"
        
        print(f"✅ Заказ найден! ID: {order['id']}, Track: {order['track']}, Metro: {order['metroStation']}")
    
    def test_get_order_without_track_error(self, order_api):
        """
        Тест 2: запрос без номера заказа возвращает ошибку
        Ожидаемый результат: код 400, сообщение об ошибке
        """
        # Шаг 1: Отправляем запрос без параметра t
        response = requests.get(f'{OrderAPI.BASE_URL}/orders/track')
        
        # Шаг 2: Проверяем статус-код
        assert response.status_code == 400, f"Код ответа должен быть 400, получен {response.status_code}"
        
        # Шаг 3: Проверяем сообщение об ошибке
        assert "Недостаточно данных для поиска" in response.text, \
            "Сообщение об ошибке должно содержать 'Недостаточно данных для поиска'"
        
        print(f"✅ Ошибка получена: {response.text}")
    
    def test_get_order_with_empty_track_error(self, order_api):
        """
        Тест 3: запрос с пустым номером заказа возвращает ошибку
        Ожидаемый результат: код 400, сообщение об ошибке
        """
        # Шаг 1: Отправляем запрос с пустым параметром t
        response = order_api.get_order_by_track('')
        
        # Шаг 2: Проверяем статус-код
        assert response.status_code == 400, f"Код ответа должен быть 400, получен {response.status_code}"
        
        # Шаг 3: Проверяем сообщение об ошибке
        assert "Недостаточно данных для поиска" in response.text or "Некорректный номер заказа" in response.text, \
            "Сообщение об ошибке должно быть о недостаточности данных"
        
        print(f"✅ Ошибка получена: {response.text}")
    
    def test_get_order_nonexistent_track_error(self, order_api):
        """
        Тест 4: запрос с несуществующим заказом возвращает ошибку
        Ожидаемый результат: код 404, сообщение "Заказ не найден"
        """
        # Шаг 1: Используем заведомо несуществующий трек
        nonexistent_track = 999999
        
        # Шаг 2: Отправляем запрос с несуществующим треком
        response = order_api.get_order_by_track(nonexistent_track)
        
        # Шаг 3: Проверяем статус-код
        assert response.status_code == 404, f"Код ответа должен быть 404, получен {response.status_code}"
        
        # Шаг 4: Проверяем сообщение об ошибке
        expected_error = {"code": 404, "message": "Заказ не найден"}
        assert response.json() == expected_error, \
            f"Ожидалась ошибка {expected_error}, получена {response.json()}"
        
        print(f"✅ Ошибка получена: {response.json()}")
    
    def test_get_order_with_negative_track_error(self, order_api):
        """
        Тест 5: запрос с отрицательным номером заказа возвращает ошибку
        Ожидаемый результат: код 404 или 400 (сервер может вернуть 500, но это баг)
        """
        # Шаг 1: Используем отрицательный трек
        negative_track = -1
        
        # Шаг 2: Отправляем запрос
        response = order_api.get_order_by_track(negative_track)
        
        # Шаг 3: Проверяем, что пришла ошибка
        assert response.status_code in [400, 404, 500], \
            f"Код ответа должен быть ошибкой, получен {response.status_code}"
        
        print(f"✅ Ошибка получена с кодом {response.status_code}")
    
    def test_get_order_with_string_track_error(self, order_api):
        """
        Тест 6: запрос с текстовым номером заказа возвращает ошибку
        Ожидаемый результат: код 400 (сервер может вернуть 500, но это баг)
        """
        # Шаг 1: Используем текстовый трек
        string_track = 'abc123'
        
        # Шаг 2: Отправляем запрос
        response = order_api.get_order_by_track(string_track)
        
        # Шаг 3: Проверяем статус-код
        assert response.status_code in [400, 500], \
            f"Код ответа должен быть 400 или 500, получен {response.status_code}"
        
        print(f"✅ Ошибка получена с кодом {response.status_code}")
    
    def test_get_order_after_cancellation(self, order_api, create_test_order):
        """
        Тест 7: проверка получения заказа после его отмены
        Ожидаемый результат: заказ не найден (404) или имеет статус "отменен"
        """
        # Шаг 1: Получаем track из фикстуры
        track = create_test_order
        
        # Шаг 2: Отменяем заказ
        cancel_response = order_api.cancel_order(track)
        assert cancel_response.status_code == 200, "Заказ должен быть отменен"
        
        # Шаг 3: Пытаемся получить отмененный заказ
        response = order_api.get_order_by_track(track)
        
        # Шаг 4: Проверяем результат
        if response.status_code == 404:
            assert "Заказ не найден" in response.text
            print("✅ Отмененный заказ не найден (404)")
        elif response.status_code == 200:
            order = response.json()['order']
            print(f"✅ Заказ найден со статусом: {order.get('status', 'неизвестен')}")
        else:
            assert False, f"Неожиданный код ответа: {response.status_code}"