from rest_framework import serializers
from .models import Property, Room, PropertyImage , RoomImage




import json

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

    uploaded_images = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Property
        fields = '__all__'

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images', [])

        property_obj = Property.objects.create(**validated_data)

        for img in images:
            PropertyImage.objects.create(property=property_obj, image=img)

        return property_obj

    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for img in images:
            PropertyImage.objects.create(property=instance, image=img)

        return instance


class RoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)

    uploaded_images = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    class Meta:
        model = Room
        fields = '__all__'

    def validate_uploaded_images(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least 1 image required")
        if len(value) > 5:
            raise serializers.ValidationError("Max 5 images allowed")
        return value

    def validate(self, data):
        request = self.context['request']
        property_obj = data.get('property')

        if property_obj.owner != request.user:
            raise serializers.ValidationError("You cannot add room to this property")

        return data

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images')

        room = Room.objects.create(**validated_data)

        for img in images:
            RoomImage.objects.create(room=room, image=img)

        return room
