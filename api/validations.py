from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


class ValidateEmployeeMixin:
    @staticmethod
    def validate_employees(employees):
        deleted_employees = User.objects.filter(
            portal_user_id__in=employees, deleted=True
        )
        if deleted_employees:
            raise ValidationError("You cannot add remote employees")
        return employees
