from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView

from . import api_views


urlpatterns = [
    path('api/', api_views.CustomSpectacularAPIView.as_view(), name='api-root-schema'),
    path('api/schema/', api_views.CustomSpectacularAPIView.as_view(), name='api-schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='swagger-ui'),
    path('api/$app_name_lowercase/', api_views.${app_name_capitalized}ListCreateView.as_view(), name='$app_name_lowercase-list-create'),
]
