
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json

class AuthTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_user_default_organisation(self):
        data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('accessToken', response.data['data'])

    def test_login_user_success(self):
        data = {
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data['data'])

    def test_register_missing_required_fields(self):
        data = {
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_register_duplicate_email_or_userid(self):
        data1 = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }
        data2 = {
            'firstName': 'Jane',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'anothersecurepassword'
        }
        self.client.post(self.register_url, data1, format='json')
        response = self.client.post(self.register_url, data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
