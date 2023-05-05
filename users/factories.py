import uuid

import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "Employee_{}".format(n))
    portal_user_id = factory.LazyFunction(uuid.uuid4)
    email = factory.Sequence(lambda n: "user_{}@example.com".format(n))
    phone = factory.Sequence(lambda n: "790255549%02d" % n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
