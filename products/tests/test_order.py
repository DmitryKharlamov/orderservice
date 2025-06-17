import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from subscriptions.models import Tariff, UserSubscription
from django.utils import timezone
from datetime import timedelta


User = get_user_model()

@pytest.mark.django_db
def test_create_order():
    client = APIClient()

    # Создаём пользователя
    user = User.objects.create_user(
        username='testuser',
        password='testpass',
        phone='88005553535'
    )

    # Логинимся (используется сессионная аутентификация)
    client.login(username='testuser', password='testpass')

    # Создаём тариф
    tariff = Tariff.objects.create(
        name='Базовый',
        description='Тестовый тариф',
        price=100,
        duration_days=30
    )

    # Создаём подписку
    UserSubscription.objects.create(
        user=user,
        tariff=tariff,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=tariff.duration_days)
    )

    # Данные заказа
    data = {
        'product_name': 'Пицца',
        'quantity': 2
    }

    # Делаем POST-запрос
    response = client.post('/api/orders/', data)


    assert response.status_code == 201
    assert response.data['product_name'] == 'Пицца'
    assert response.data['quantity'] == 2


    # Делаем GET-запрос
    response = client.get('/api/orders/')
    assert response.status_code == 200
    assert any(order['product_name'] == 'Пицца' for order in response.data)