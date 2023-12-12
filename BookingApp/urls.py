from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views
from .views import register_user, delete_user


urlpatterns = [
    # вивід готелів, кімнат, бронювань і їх деталей
    path('hotels/', views.HotelListView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel-detail'),
    path('rooms/', views.RoomListView.as_view(), name='room-list'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room-detail'),
    path('reservations/', views.ReservationListView.as_view(), name='reservation-list'),
    path('reservation/<int:pk>/', views.ReservationDetailView.as_view(), name='reservation-detail'),
    # аутентифікація звичайна по логіну та паролю
    path('drf-auth/', include('rest_framework.urls')),
    # реєстрація користувача POST запит email, first_name, last_name, password
    path('register/', register_user, name='register_user'),
    # користувач може видалити сам себе по бажанню
    path('delete-user/', delete_user, name='delete-user'),
    # авторизація за допомогою jwt token / POST запит, передаємо username і password
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # оновлення access токену, передаємо refresh token і отримуємо новий access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]