import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from organizations.factories import OrganizationFactory
from organizations.models import Organization, Requisites
from users.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestOrganizations:
    def test_get_list_organizations_without_token(self, client):
        url = reverse("api:organization-list")
        OrganizationFactory.create_batch(5)

        response = client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {
            "detail": "You do not have permission to perform this action."
        }

    def test_get_list_organizations(self, client, headers):
        url = reverse("api:organization-list")
        _ = OrganizationFactory.create_batch(5)

        response = client.get(url, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert Organization.objects.count() == len(response.json())

    def test_get_organization(self, client, headers):
        organization = OrganizationFactory()
        url = reverse("api:organization-detail", kwargs={"pk": organization.id})

        response = client.get(url, headers=headers)

        content = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert content["id"] == str(organization.id)

    def test_update_organization(self, client, headers):
        employees = UserFactory.create_batch(3)
        organization = OrganizationFactory.create(add_employees=employees)
        Requisites.objects.create(
            name="name", value="name organization", organization=organization
        )
        new_requisites = [
            {"name": "inn", "value": "23423424"},
            {"name": "name", "value": "new name organization"},
        ]
        payload = {
            "requisites": new_requisites,
        }
        url = reverse("api:organization-detail", kwargs={"pk": organization.id})

        response = client.patch(
            url, data=payload, content_type="application/json", headers=headers
        )

        organization.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert list(organization.requisites.values("value", "name")) == new_requisites

    def test_create_organization(self, client, headers):
        UserFactory(is_superuser=True)
        portal_user_id = uuid.uuid4()
        employee = UserFactory(portal_user_id=portal_user_id)
        payload = {
            "product_name": "test_name",
            "requisites": [
                {"name": "name", "value": "name_organization"},
                {"name": "inn", "value": "23423424"},
            ],
            "employees": [employee.portal_user_id],
        }
        url = reverse("api:organization-list")

        response = client.post(
            url, data=payload, content_type="application/json", headers=headers
        )

        organization = Organization.objects.last()

        assert response.status_code == status.HTTP_201_CREATED
        assert Organization.objects.count() == 1
        assert list(
            organization.employees.values_list("portal_user_id", flat=True)
        ) == [portal_user_id]

    def test_create_organization_with_deleted_employee(self, client, headers):
        UserFactory(is_superuser=True)
        portal_user_id = uuid.uuid4()
        employee = UserFactory(portal_user_id=portal_user_id, deleted=True)
        payload = {
            "product_name": "test_name",
            "requisites": [
                {"name": "name", "value": "name_organization"},
                {"name": "inn", "value": "23423424"},
            ],
            "employees": [employee.portal_user_id],
        }
        url = reverse("api:organization-list")

        response = client.post(
            url, data=payload, content_type="application/json", headers=headers
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Organization.objects.count() == 0
        assert response.json() == {"employees": ["You cannot add remote employees"]}

    def test_add_employees(self, client, headers):
        employees = UserFactory.create_batch(3)
        organization = OrganizationFactory.create(add_employees=employees)
        new_employees = UserFactory.create_batch(2)
        payload = {
            "employees": [str(employee.portal_user_id) for employee in new_employees]
        }
        url = reverse("api:organization-add-employees", kwargs={"pk": organization.id})

        response = client.patch(
            url, data=payload, content_type="application/json", headers=headers
        )

        organization.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert organization.employees.count() == len(employees + new_employees)

    def test_add_deleted_employees(self, client, headers):
        employees = UserFactory.create_batch(3)
        organization = OrganizationFactory.create(add_employees=employees)
        new_employees = UserFactory.create_batch(2, deleted=True)
        payload = {
            "employees": [str(employee.portal_user_id) for employee in new_employees]
        }
        url = reverse("api:organization-add-employees", kwargs={"pk": organization.id})

        response = client.patch(
            url, data=payload, content_type="application/json", headers=headers
        )

        organization.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert organization.employees.count() == len(employees)
        assert response.json() == {"employees": ["You cannot add remote employees"]}
