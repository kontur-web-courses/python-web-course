from datetime import datetime

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework.permissions import BasePermission

from tokens.models import Token


class KeyPermissions(BasePermission):
    def has_permission(self, request, view) -> bool:
        if "Token" in request.headers:
            token_request = request.headers.get("Token")
            token_db = Token.objects.first()
            try:
                payload = jwt.decode(
                    token_request, token_db.secret, algorithms=[settings.JWT_ALGORITHM]
                )
            except Exception:
                return False
            expired: int = payload.get("exp", 0)
            if datetime.fromtimestamp(expired, tz=timezone.utc) > datetime.now(
                tz=timezone.utc
            ):
                return True

        return False
