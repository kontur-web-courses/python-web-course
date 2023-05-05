from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.permissions import KeyPermissions
from api.serializers import (
    CreateEmployeeSerializer,
    ListEmployeeSerializer,
    UpdateEmployeeSerializer,
)

User = get_user_model()


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="List employees",
        operation_description="Get list employees",
        responses={status.HTTP_200_OK: ListEmployeeSerializer()},
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="One employee",
        operation_description="Get one employee by portal_user_id",
        responses={
            status.HTTP_200_OK: ListEmployeeSerializer(),
            status.HTTP_404_NOT_FOUND: "Organization by portal_user_id not found",
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Сreate a new employee",
        operation_description="Сreate a new employee",
        responses={
            status.HTTP_200_OK: CreateEmployeeSerializer(),
            status.HTTP_400_BAD_REQUEST: "Data is not valid",
        },
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Update employee",
        operation_description="Update employee by portal_user_id",
        responses={
            status.HTTP_200_OK: ListEmployeeSerializer(),
            status.HTTP_400_BAD_REQUEST: "Data is not valid",
        },
    ),
)
class EmployeesViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = User.objects.filter(is_superuser=False)
    permission_classes = [KeyPermissions]
    lookup_field = "portal_user_id"

    def get_serializer_class(self):
        matcher = {
            "create": CreateEmployeeSerializer,
            "partial_update": UpdateEmployeeSerializer,
        }
        return matcher.get(self.action, ListEmployeeSerializer)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        organization = self.get_object()
        serializer = self.get_serializer(organization, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = ListEmployeeSerializer(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)
