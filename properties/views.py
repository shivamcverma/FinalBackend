from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Property, Room
from .serializers import PropertySerializer, RoomSerializer
from .permissions import IsOwnerOrReadOnly

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Property.objects.none()

        if self.request.user.is_authenticated:
            return Property.objects.filter(owner=self.request.user)

        return Property.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Room.objects.none()

        if self.request.user.is_authenticated:
            return Room.objects.filter(property__owner=self.request.user)

        return Room.objects.none()