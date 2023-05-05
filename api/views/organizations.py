import uuid

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
    CreateOrganizationSerializer,
    ListOrganizationSerializer,
    OrganizationAddEmployeeSerializer,
    UpdateOrganizationSerializer,
)
from organizations.models import Organization, Requisites

User = get_user_model()


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="List organizations",
        operation_description="Get list organizations",
        responses={status.HTTP_200_OK: ListOrganizationSerializer()},
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="One organization",
        operation_description="Get one organization by id",
        responses={
            status.HTTP_200_OK: ListOrganizationSerializer(),
            status.HTTP_404_NOT_FOUND: "Organization by ID not found",
        },
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Сreate a new organization",
        operation_description="Сreate a new organization",
        responses={
            status.HTTP_200_OK: CreateOrganizationSerializer(),
            status.HTTP_400_BAD_REQUEST: "Data is not valid",
        },
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Update organization",
        operation_description="Update organization",
        responses={
            status.HTTP_200_OK: UpdateOrganizationSerializer(),
            status.HTTP_400_BAD_REQUEST: "Data is not valid",
        },
    ),
)
class OrganizationsViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = Organization.objects.all()
    permission_classes = [KeyPermissions]

    def get_serializer_class(self):
        matcher = {
            "create": CreateOrganizationSerializer,
            "partial_update": UpdateOrganizationSerializer,
            "add_employee": OrganizationAddEmployeeSerializer,
        }
        return matcher.get(self.action, ListOrganizationSerializer)

    @swagger_auto_schema(
        operation_summary="Add employee to organization",
        operation_description="Add employee to organization",
        request_body=OrganizationAddEmployeeSerializer,
        responses={
            status.HTTP_200_OK: ListOrganizationSerializer(),
            status.HTTP_400_BAD_REQUEST: "Data is not valid",
            status.HTTP_404_NOT_FOUND: "Organization by ID not found",
        },
    )
    @action(detail=True, methods=["patch"], url_name="add-employees")
    def add_employee(self, request, pk):
        organization = self.get_object()
        serializer = self.get_serializer(organization, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        employees = serializer.validated_data.get("employees")
        organization.employees.add(*User.objects.filter(portal_user_id__in=employees))
        serializer = ListOrganizationSerializer(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        organization = self.get_object()
        serializer = self.get_serializer(organization, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        for requisite in serializer.validated_data.get("requisites"):
            Requisites.objects.update_or_create(
                name=requisite["name"],
                organization=organization,
                defaults={"value": requisite["value"]},
            )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = Organization.objects.create(
            id=uuid.uuid4(),
            product_name=serializer.validated_data.get("product_name"),
            created_by_user=User.objects.filter(is_superuser=True).first(),
        )
        Requisites.objects.bulk_create(
            [
                Requisites(
                    name=requisite["name"],
                    value=requisite["value"],
                    organization=organization,
                )
                for requisite in serializer.validated_data.get("requisites")
            ]
        )
        employees = serializer.validated_data.get("employees")
        if employees:
            organization.employees.add(
                *User.objects.filter(portal_user_id__in=employees)
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
