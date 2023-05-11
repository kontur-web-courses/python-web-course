from django.contrib.auth import get_user_model
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import RoleOperations

User = get_user_model()


class ListEmployeeSerializer(ModelSerializer):
    operations = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "portal_user_id",
            "email",
            "phone",
            "role",
            "operations",
            "deleted",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def get_operations(obj):
        return RoleOperations.objects.filter(role__in=obj.role).values_list(
            "operations", flat=True
        )


class CreateEmployeeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "portal_user_id",
            "email",
            "phone",
            "role",
        )
        extra_kwargs = {
            "portal_user_id": {"required": True},
            "email": {"required": True},
            "role": {"required": True},
            "phone": {"required": False},
        }


class UpdateEmployeeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "phone",
            "role",
            "deleted",
        )
