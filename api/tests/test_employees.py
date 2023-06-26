import uuid

import pytest
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework import status

from tokens.models import Token
from users.factories import UserFactory
from users.models import Roles

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestEmployees:
    def test_get_list_employees(self, client, headers):
        url = reverse("api:employee-list")
        _ = UserFactory.create_batch(6)

        response = client.get(url, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert User.objects.filter(is_superuser=False).count() == len(response.json())

    def test_get_employee(self, client, headers):
        employee = UserFactory()
        url = reverse(
            "api:employee-detail", kwargs={"portal_user_id": employee.portal_user_id}
        )

        response = client.get(url, headers=headers)

        content = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert content["portal_user_id"] == str(employee.portal_user_id)

    def test_update_employee(self, client):
        employee = UserFactory(deleted=False, role=Roles.USER, phone="999999999")
        url = reverse(
            "api:employee-detail", kwargs={"portal_user_id": employee.portal_user_id}
        )
        payload = {
            "phone": "89025123456",
            "role": Roles.APPROVER,
        }
        employee_data = model_to_dict(employee)
        employee_data.update(payload)

        response = client.patch(
            url,
            data=payload,
            content_type="application/json",
            headers={"Token": Token.objects.first().jwt},
        )

        employee.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert employee_data == model_to_dict(employee)

    def test_create_employee(self, client, headers):
        url = reverse("api:employee-list")
        payload = {
            "portal_user_id": uuid.uuid4(),
            "email": "test_create@mail.ru",
            "phone": "89025123456",
            "role": Roles.USER,
            "username": "test_user",
        }
        response = client.post(
            url, data=payload, content_type="application/json", headers=headers
        )

        employee = User.objects.last()

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        assert employee.email == payload["email"]
        assert employee.phone == payload["phone"]
        assert employee.role == payload["role"]
