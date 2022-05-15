from django.test import Client, TestCase
from django.contrib.auth import get_user_model
# import pytest

User = get_user_model()

class UsersApi(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)


    def test_users_list(self):                        
        response = self.guest_client.get('/api/users/?limit=5')
        self.assertEqual(response.status_code, 200,'Неавторизованному пользователю недоступен список пользователей')
        response = self.authorized_client.get('/api/users/?limit=5')
        self.assertEqual(response.status_code, 200, 'Авторизованному пользователю недоступен список пользователей')
