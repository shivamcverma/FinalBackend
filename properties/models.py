from django.db import models
from users.models import User


class Property(models.Model):
    PROPERTY_TYPES = (
        ('HOSTEL', 'Hostel'),
        ('PG', 'PG'),
        ('ROOM', 'Room'),
        ('FLAT', 'Flat'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    amenities = models.JSONField(default=list, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Room(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.CharField(max_length=50)
    capacity = models.IntegerField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.property.title} - Room {self.room_number}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='property_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='room_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)