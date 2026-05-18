from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Property, Room
from .serializers import PropertySerializer, RoomSerializer
from .permissions import IsOwnerOrReadOnly
from .models import PropertyImage, RoomImage

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

        property_obj = serializer.save(owner=self.request.user)

        images = self.request.FILES.getlist('uploaded_images')

        for img in images:
            PropertyImage.objects.create(
                property=property_obj,
                image=img
            )

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
    def perform_create(self, serializer):

        room = serializer.save()

        images = self.request.FILES.getlist('uploaded_images')

        for img in images:
            RoomImage.objects.create(
                room=room,
                image=img
            )