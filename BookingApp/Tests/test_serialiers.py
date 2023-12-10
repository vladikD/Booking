from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from BookingApp.models import Hotel,Room
from BookingApp.serializers import HotelSerializer,RoomSerializer
class UserRegistrationSerializerTest(APITestCase):

    def test_valid_user_registration(self):
        data = {'email': 'test@gmail.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'password123'}
        response = self.client.post('/api/booking/register/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.email, 'test@gmail.com')

    def test_invalid_name_format(self):
        data = {'email': 'test@gmail.com', 'first_name': 'John#', 'last_name': 'Doe', 'password': 'password123'}
        response = self.client.post('/api/booking/register/', data, format='json')
        print(response.data)  # Вивести дані в консоль
        self.assertEqual(response.status_code, 400)
        self.assertIn('Неприпустимий формат імені.', response.data['first_name'][0])

    def test_invalid_email(self):
        data = {'email': 'test@example.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'password123'}
        response = self.client.post('/api/booking/register/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Електронна пошта повинна закінчуватися на @gmail.com.', response.data['email'][0])

    def test_invalid_password(self):
        data = {'email': 'test@gmail.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'short'}
        response = self.client.post('/api/booking/register/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Пароль повинен бути не менше 8 символів.', response.data['password'][0])

    def test_unique_email(self):
        # Створення користувача з тією ж електронною поштою
        User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='password123')
        data = {'email': 'test@gmail.com', 'first_name': 'John', 'last_name': 'Doe', 'password': 'password123'}
        response = self.client.post('/api/booking/register/', data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertIn('User with this email already exists.', response.data['error'])


class HotelSerializerTest(APITestCase):

    def test_valid_hotel_serializer(self):
        data = {'name': 'Khreschatyk Hotel', 'address': 'вулиця Хрещатик, 14, Київ'}
        serializer = HotelSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_hotel_name(self):
        data = {'name': '', 'address': 'вулиця Хрещатик, 14, Київ'}
        serializer = HotelSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('This field may not be blank.', serializer.errors['name'])

    def test_invalid_hotel_address(self):
        data = {'name': 'Khreschatyk Hotel', 'address': ''}
        serializer = HotelSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('This field may not be blank.', serializer.errors['address'])

    def test_create_hotel(self):
        data = {'name': 'Khreschatyk Hotel', 'address': 'вулиця Хрещатик, 14, Київ'}
        serializer = HotelSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        hotel = serializer.save()
        self.assertIsInstance(hotel, Hotel)
        self.assertEqual(hotel.name, 'Khreschatyk Hotel')
        self.assertEqual(hotel.address, 'вулиця Хрещатик, 14, Київ')

class RoomSerializerTest(APITestCase):

    def test_valid_room_serializer(self):
        # Створення об'єкта Hotel
        hotel = Hotel.objects.create(name='Hotel A', address='Address A')

        data = {'hotel': hotel.pk, 'room_number': '101', 'room_type': 'Single', 'price_per_night': 100.0}
        serializer = RoomSerializer(data=data)
        is_valid = serializer.is_valid()
        if not is_valid:
            print(serializer.errors)
        self.assertTrue(is_valid)

    def test_invalid_room_number_blank(self):
        data = {'hotel': 'Hotel A', 'room_number': '', 'room_type': 'Single', 'price_per_night': 100.0}
        serializer = RoomSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('This field may not be blank.', serializer.errors['room_number'])

    def test_invalid_room_type_blank(self):
        data = {'hotel': 'Hotel A', 'room_number': '101', 'room_type': '', 'price_per_night': 100.0}
        serializer = RoomSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('This field may not be blank.', serializer.errors['room_type'])

    def test_invalid_price_per_night_invalid(self):
        data = {'hotel': 'Hotel A', 'room_number': '101', 'room_type': 'Single', 'price_per_night': 'invalid'}
        serializer = RoomSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('A valid number is required.', serializer.errors['price_per_night'][0])

    def test_create_room(self):
        # Створюємо об'єкт Hotel
        hotel = Hotel.objects.create(name='Hotel A', address='Address A')

        # Створюємо кімнату
        room_data = {'hotel': hotel.pk, 'room_number': '101', 'room_type': 'Single', 'price_per_night': 100.0}
        room_serializer = RoomSerializer(data=room_data)
        self.assertTrue(room_serializer.is_valid())
        room = room_serializer.save()
