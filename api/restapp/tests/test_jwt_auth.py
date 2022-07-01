import re

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.test import TestCase


class JWTTests(TestCase):

    default_password = 'password'

    def create_user(self, email, password):
        user_model = get_user_model()
        return user_model.objects.create_user(email=email, password=password)


    def test_no_account_returns_401(self):
        response = self.client.post('/api/token/', {'email': 'not@exists', 'password': 'password'}, format='json')

        assert response.status_code == 401
        assert response.data['detail'] == 'No active account found with the given credentials'

    def test_user_can_get_jwt(self):

        user = self.create_user('test@test.com', self.default_password)
        response = self.client.post('/api/token/', {'email': user.email, 'password': self.default_password}, format='json')
        assert response.status_code == 200
        assert 'access' in response.data
        assert re.match('^[\w-]*\.[\w-]*\.[\w-]*$', response.data['access'])

    def test_user_can_access_protected_endpoint_with_jwt(self):

        user = self.create_user('test@test.com', self.default_password)
        response = self.client.post('/api/token/', {'email': user.email, 'password': self.default_password}, format='json')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = client.get('/api/token/authcheck/')
        assert response.status_code == 200

    def test_user_can_refresh_jwt(self):

        user = self.create_user('test@test.com', self.default_password)
        response = self.client.post('/api/token/', {'email': user.email, 'password': self.default_password}, format='json')
        response = self.client.post('/api/token/refresh/', {'refresh': response.data['refresh']})
        assert 'access' in response.data
        assert re.match('^[\w-]*\.[\w-]*\.[\w-]*$', response.data['access'])


