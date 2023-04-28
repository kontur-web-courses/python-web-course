import uuid
from datetime import datetime, timedelta

import jwt
from django.contrib.auth import get_user_model
from django.utils import timezone

from organizations.factories import OrganizationFactory
from organizations.models import Organization, Requisites, RequisitesName
from tokens.models import Token
from users.factories import UserFactory
from users.models import Operations, RoleOperations, Roles
from django.conf import settings


User = get_user_model()


class GenerateDataError(Exception):
    pass


def regenerate_token() -> None:
    Token.objects.all().delete()
    now = datetime.now(tz=timezone.utc)
    payload = {
        "exp": now + timedelta(seconds=settings.JWT_EXPIRED),
    }
    secret = uuid.uuid4().hex
    Token.objects.create(
        jwt=jwt.encode(payload, secret, algorithm=settings.JWT_ALGORITHM), secret=secret
    )


def _delete_all_data_in_db() -> None:
    User.objects.filter(is_superuser=False).delete()
    Organization.objects.all().delete()
    Requisites.objects.all().delete()
    Token.objects.all().delete()
    RoleOperations.objects.all().delete()


def regenerate() -> None:
    _delete_all_data_in_db()
    superuser = User.objects.filter(is_superuser=True).first()
    if not superuser:
        raise GenerateDataError

    admin = RoleOperations.objects.create(
        role=Roles.ADMIN,
        operations=[
            Operations.ADMIN_INVITE,
            Operations.ADD_PAYMENT,
            Operations.APPROVE_PAYMENT,
            Operations.SEND_PAYMENT,
        ],
    )
    user = RoleOperations.objects.create(
        role=Roles.USER,
        operations=[
            Operations.ADD_PAYMENT,
            Operations.SEND_PAYMENT,
            Operations.CAN_VIEW_BALANCE,
        ],
    )
    approver = RoleOperations.objects.create(
        role=Roles.APPROVER, operations=[Operations.APPROVE_PAYMENT]
    )

    organizations = [
        ("Ромашка", "2463043654", "246301001", "auto"),
        ("Лютик", "8563902641", "586749032", "reestro"),
        ("Фиалка", "8563902641", "586749032", "market"),
    ]

    for name, inn, kpp, product_name in organizations:
        organization = OrganizationFactory(
            created_by_user=superuser,
            product_name=product_name,
            add_employees=[
                UserFactory(role=[admin]),
                *UserFactory.create_batch(2, role=[user]),
                UserFactory(role=[approver]),
            ],
        )
        Requisites.objects.create(
            organization=organization, name=RequisitesName.NAME, value=name
        )
        Requisites.objects.create(
            organization=organization, name=RequisitesName.INN, value=inn
        )
        Requisites.objects.create(
            organization=organization, name=RequisitesName.KPP, value=kpp
        )

    UserFactory.create_batch(4)
    UserFactory.create_batch(3, deleted=True)
    regenerate_token()
