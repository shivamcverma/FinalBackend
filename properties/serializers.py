from rest_framework import serializers
from .models import Property, Room, PropertyImage, RoomImage


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'uploaded_at']


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['id', 'image']


class PropertySerializer(serializers.ModelSerializer):

    images = PropertyImageSerializer(many=True, read_only=True)

    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['owner']


class RoomSerializer(serializers.ModelSerializer):

    images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['owner']
    def validate(self, data):

        request = self.context['request']
        property_obj = data.get('property')

        if property_obj.owner != request.user:
            raise serializers.ValidationError(
                "You cannot add room to this property"
            )

        return data