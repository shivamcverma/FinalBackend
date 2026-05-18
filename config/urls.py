from django.urls import path, include
from django.contrib import admin
from drf_yasg.views import get_schema_view, schema_view
from drf_yasg import openapi

from properties import permissions


# 🔥 SWAGGER CONFIG
schema_view = get_schema_view(
    openapi.Info(
        title="Tolet API",
        default_version='v1',
        description="Tolet Backend APIs",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/properties/', include('properties.urls')),
    path(
    'swagger/',
    schema_view.with_ui(
        'swagger',
        cache_timeout=0
    )
),
]


