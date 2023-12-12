#_____________Django_Rest_Framework_______
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

#______________Django______________________
from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

#___________OTHER___________________________
from .models import Hotel, Room, Reservation
from .serializers import HotelSerializer, RoomSerializer, ReservationSerializer, UserSerializer, UserRegistrationSerializer

#___________SWAGGER_________________________
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='delete',
    operation_description="Delete the authenticated user",
    responses={204: 'No Content', 403: 'Permission denied'}
)
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    user_to_delete = request.user  # Отримання користувача, який намагається видалити свій обліковий запис

    # Перевірка, чи користувач спробує видалити себе
    if user_to_delete == request.user:
        user_to_delete.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='post',
    operation_description="Register a new user",
    request_body=UserRegistrationSerializer,
    responses={201: 'Created', 400: 'Bad Request'}
)
@api_view(['POST'])
def register_user(request):
    # Перевірка наявності користувача з таким самим email
    existing_user = User.objects.filter(email=request.data.get('email')).first()
    if existing_user:
        return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class HotelListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a list of hotels",
        responses={200: openapi.Response('List of hotels', HotelSerializer(many=True))}
    )
    def get(self, request, format=None):
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new hotel",
        request_body=HotelSerializer,
        responses={201: 'Created', 400: 'Bad Request'}
    )
    def post(self, request, format=None):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class HotelDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of a specific hotel",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Hotel ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response('Hotel details', HotelSerializer)}
    )
    def get(self, request, pk, format=None):
        hotel = get_object_or_404(Hotel, pk=pk)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update details of a specific hotel",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Hotel ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=HotelSerializer,
        responses={200: 'Updated', 400: 'Bad Request'}
    )
    def put(self, request, pk, format=None):
        hotel = get_object_or_404(Hotel, pk=pk)
        serializer = HotelSerializer(hotel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific hotel",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Hotel ID", type=openapi.TYPE_INTEGER),
        ],
        responses={204: 'No Content'}
    )
    def delete(self, request, pk, format=None):
        hotel = get_object_or_404(Hotel, pk=pk)
        hotel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class RoomListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a list of rooms",
        responses={200: openapi.Response('List of rooms', RoomSerializer(many=True))}
    )
    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new room",
        request_body=RoomSerializer,
        responses={201: 'Created', 400: 'Bad Request'}
    )
    def post(self, request, format=None):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of a specific room",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Room ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response('Room details', RoomSerializer)}
    )
    def get(self, request, pk, format=None):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update details of a specific room",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Room ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=RoomSerializer,
        responses={200: 'Updated', 400: 'Bad Request'}
    )
    def put(self, request, pk, format=None):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific room",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Room ID", type=openapi.TYPE_INTEGER),
        ],
        responses={204: 'No Content'}
    )
    def delete(self, request, pk, format=None):
        room = get_object_or_404(Room, pk=pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReservationListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Get a list of reservations",
        responses={200: openapi.Response('List of reservations', ReservationSerializer(many=True))}
    )
    def get(self, request, format=None):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new reservation",
        request_body=ReservationSerializer,
        responses={201: 'Created', 400: 'Bad Request'}
    )
    def post(self, request, format=None):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=request.user)  # Використовую client для збереження користувача
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ReservationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get details of a specific reservation",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Reservation ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: openapi.Response('Reservation details', ReservationSerializer)}
    )
    def get(self, request, pk, format=None):
        reservation = get_object_or_404(Reservation, pk=pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update details of a specific reservation",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Reservation ID", type=openapi.TYPE_INTEGER),
        ],
        request_body=ReservationSerializer,
        responses={200: 'Updated', 400: 'Bad Request'}
    )
    def patch(self, request, pk, format=None):
        reservation = get_object_or_404(Reservation, pk=pk)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a specific reservation",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Reservation ID", type=openapi.TYPE_INTEGER),
        ],
        responses={204: 'No Content'}
    )
    def delete(self, request, pk, format=None):
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
