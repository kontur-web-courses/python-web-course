from django.contrib.auth import get_user_model
from rest_framework.fields import CharField, ListField
from rest_framework.serializers import ModelSerializer

from api.serializers.employees import ListEmployeeSerializer
from api.validations import ValidateEmployeeMixin
from organizations.models import Organization, Requisites

User = get_user_model()


class RequisitesSerializer(ModelSerializer):
    class Meta:
        model = Requisites
        fields = ("name", "value")


class ListOrganizationSerializer(ModelSerializer):
    employees = ListEmployeeSerializer(many=True, required=False)
    requisites = RequisitesSerializer(many=True)

    class Meta:
        model = Organization
        fields = (
            "id",
            "product_name",
            "requisites",
            "employees",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "id": {"required": False, "read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class UpdateOrganizationSerializer(ModelSerializer):
    requisites = RequisitesSerializer(many=True)

    class Meta:
        model = Organization
        fields = ("requisites",)


class OrganizationAddEmployeeSerializer(ModelSerializer, ValidateEmployeeMixin):
    employees = ListField(
        child=CharField(),
        required=False,
    )

    class Meta:
        model = Organization
        fields = ("employees",)


class CreateOrganizationSerializer(ModelSerializer, ValidateEmployeeMixin):
    requisites = RequisitesSerializer(many=True)
    employees = ListField(
        child=CharField(),
        required=False,
    )

    class Meta:
        model = Organization
        fields = (
            "product_name",
            "requisites",
            "employees",
        )
        extra_kwargs = {"employees": {"required": False}}
