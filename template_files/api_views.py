from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.plumbing import (
    normalize_result_object, sanitize_result_object,
)

from .serializers import ${app_name_capitalized}Serializer


class ${app_name_capitalized}ListCreateView(generics.ListCreateAPIView):
    queryset = []  # Replace with your actual queryset
    serializer_class = ${app_name_capitalized}Serializer


class FilteredSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, public=False):
        """ Generate an OpenAPI schema for just the $app_name app. """
        result = super().get_schema(request, public)
        filtered_paths = {}
        for path, path_data in result['paths'].items():
            if '/$app_name_lowercase/' in path:
                filtered_paths[path] = path_data
        result['paths'] = filtered_paths
        return sanitize_result_object(normalize_result_object(result))


@extend_schema(exclude=True)
class CustomSpectacularAPIView(SpectacularAPIView):
    generator_class = FilteredSchemaGenerator
