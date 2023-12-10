from rest_framework.test import APITestCase
from django.contrib.auth.models import User



class UserRegistrationViewTest(APITestCase):

    def test_valid_user_registration(self):
        data = {'email': 'test@gmail.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'password123'}
        response = self.client.post('/api/booking/register/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.email, 'test@gmail.com')

    def test_duplicate_email_registration(self):
        # Створюємо користувача з таким же email
        User.objects.create(email='test@gmail.com', password='password123')

        # Передаємо дані для реєстрації з тим же email
        data = {'email': 'test@gmail.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'password123'}
        response = self.client.post('/api/booking/register/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'User with this email already exists.')
