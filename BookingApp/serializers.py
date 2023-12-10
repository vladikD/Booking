from django.contrib.auth.models import User
from rest_framework import serializers
from BookingApp.models import Hotel, Room, Reservation


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def validate_email(self, value):
        # Кастомна валідація для формату електронної пошти
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError('Електронна пошта повинна закінчуватися на @gmail.com.')
        return value

    def validate_first_name(self, value):
        # Ваша логіка валідації імені, наприклад, чи містить лише букви
        if not value.isalpha():
            raise serializers.ValidationError('Неприпустимий формат імені.')
        return value

    def validate_password(self, value):
        # Кастомна валідація для паролю (перевірка довжини паролю)
        if len(value) < 8:
            raise serializers.ValidationError('Пароль повинен бути не менше 8 символів.')
        return value

    def validate(self, data):
        # Перевірка, чи користувач з таким ім'ям вже існує
        username = data.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Користувач з таким іменем вже існує.')
        return data
    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name', 'address']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['hotel', 'room_number', 'room_type', 'price_per_night']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['hotel', 'room', 'client', 'check_in_date', 'check_out_date']