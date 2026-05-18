from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied

from .models import (
    Property,
    Room,
    PropertyImage,
    RoomImage
)

from .serializers import (
    PropertySerializer,
    RoomSerializer
)

from .permissions import (
    IsOwnerOrReadOnly
)


class PropertyViewSet(viewsets.ModelViewSet):

    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Property.objects.none()

        user = self.request.user

        queryset = Property.objects.prefetch_related(
            'images',
            'rooms__images'
        )

        if user.is_authenticated and user.role == 'OWNER':
            return queryset.filter(owner=user)

        return queryset

    def perform_create(self, serializer):

        property_obj = serializer.save(
            owner=self.request.user
        )

        images = self.request.FILES.getlist(
            'uploaded_images'
        )

        for img in images:
            PropertyImage.objects.create(
                property=property_obj,
                image=img
            )

    def perform_update(self, serializer):

        property_obj = self.get_object()

        if property_obj.owner != self.request.user:
            raise PermissionDenied(
                "You do not own this property."
            )

        serializer.save()

    def perform_destroy(self, instance):

        if instance.owner != self.request.user:
            raise PermissionDenied(
                "You do not own this property."
            )

        instance.delete()


class RoomViewSet(viewsets.ModelViewSet):

    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):

        if getattr(self, 'swagger_fake_view', False):
            return Room.objects.none()

        queryset = Room.objects.prefetch_related(
            'images'
        )

        user = self.request.user

        if user.is_authenticated and user.role == 'OWNER':
            return queryset.filter(
                property__owner=user
            )

        return queryset

    def perform_create(self, serializer):

        property_id = self.request.data.get('property')

        property_obj = Property.objects.get(
            id=property_id
        )

        if property_obj.owner != self.request.user:
            raise PermissionDenied(
                "You do not own this property."
            )

        room = serializer.save(
            property=property_obj
        )

        images = self.request.FILES.getlist(
            'uploaded_images'
        )

        for img in images:
            RoomImage.objects.create(
                room=room,
                image=img
            )

    def perform_update(self, serializer):

        room = self.get_object()

        if room.property.owner != self.request.user:
            raise PermissionDenied(
                "You do not own this room."
            )

        serializer.save()

    def perform_destroy(self, instance):

        if instance.property.owner != self.request.user:
            raise PermissionDenied(
                "You do not own this room."
            )

        instance.delete()