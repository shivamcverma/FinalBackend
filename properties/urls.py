from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, RoomViewSet

router = DefaultRouter()
router.register('properties', PropertyViewSet, basename='property')
router.register('rooms', RoomViewSet, basename='room')

urlpatterns = router.urls