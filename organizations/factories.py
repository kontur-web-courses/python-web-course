import uuid

import factory
from factory import post_generation

from organizations.models import Organization
from users.factories import UserFactory


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    id = factory.LazyFunction(uuid.uuid4)
    created_by_user = factory.SubFactory(UserFactory)

    @post_generation
    def add_employees(self, create, employees, **kwargs):
        if not create:
            return
        if employees:
            self.employees.add(*employees)
