from pytest import fixture

from tokens.models import Token


@fixture
def headers():
    return {"Token": Token.objects.first().jwt}
