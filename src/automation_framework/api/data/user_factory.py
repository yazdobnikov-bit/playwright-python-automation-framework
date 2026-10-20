import secrets
from uuid import uuid4

from automation_framework.api.models.register_user_request_schema import (
    RegisterUserRequest,
)


def build_register_user(
    first_name: str = "Test",
    last_name: str = "User",
) -> RegisterUserRequest:
    return RegisterUserRequest(
        first_name=first_name,
        last_name=last_name,
        email=f"test_{uuid4().hex}@example.com",
        password="Qa!" + secrets.token_urlsafe(24),
    )
