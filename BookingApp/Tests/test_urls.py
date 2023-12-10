from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from BookingApp.models import Hotel, Room, Reservation

class UrlsTest(TestCase):
    def setUp(self):
        # Створення тестового користувача
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Аутентифікація тестового користувача
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_hotel_list_view(self):
        response = self.client.get(reverse('hotel-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_hotel_detail_view(self):
        hotel = Hotel.objects.create(name='Test Hotel', address='123 Test St.')
        response = self.client.get(reverse('hotel-detail', kwargs={'pk': hotel.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_room_list_view(self):
        response = self.client.get(reverse('room-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_room_detail_view(self):
        room = Room.objects.create(hotel=Hotel.objects.create(name='Test Hotel', address='123 Test St.'),
                                   room_number='101', room_type='Single', price_per_night=100.0)
        response = self.client.get(reverse('room-detail', args=[room.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_list_view(self):
        response = self.client.get(reverse('reservation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_register_user_view(self):
        data = {'email': 'test@gmail.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'password123'}
        response = self.client.post(reverse('register_user'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_user_view(self):
        response = self.client.delete(reverse('delete-user'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
