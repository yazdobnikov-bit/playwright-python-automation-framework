import secrets
from uuid import uuid4

import pytest

from automation_framework.api.clients.users_api_client import UsersApiClient
from automation_framework.api.models.current_user_response_schema import (
    CurrentUserResponse,
)
from automation_framework.api.models.login_response_schema import LoginResponse


def test_login_with_valid_credentials(
    users_api: UsersApiClient,
    test_user: dict[str, str],
) -> None:
    response = users_api.login(
        {"email": test_user["email"], "password": test_user["password"]},
    )

    assert response.status == 200

    body = response.json()
    LoginResponse.model_validate(body)


def test_login_with_invalid_password(
    users_api: UsersApiClient,
    test_user: dict[str, str],
) -> None:
    response = users_api.login(
        {
            "email": test_user["email"],
            "password": test_user["password"] + "wrong",
        },
    )

    assert response.status == 401

    body = response.json()
    assert isinstance(body, dict), "Error response must be a JSON object"
    assert body["error"] == "Unauthorized"
    assert "access_token" not in body, "Failed login must not return an access token"


def test_login_with_nonexistent_user(users_api: UsersApiClient) -> None:
    response = users_api.login(
        {
            "email": f"test_{uuid4().hex}@example.com",
            "password": "Qa!" + secrets.token_urlsafe(24),
        },
    )

    assert response.status == 401

    body = response.json()
    assert isinstance(body, dict), "Error response must be a JSON object"
    assert body["error"] == "Unauthorized"
    assert "access_token" not in body, "Failed login must not return an access token"


@pytest.mark.parametrize(
    "payload, expected_error",
    [
        pytest.param({}, "Invalid login request", id="missing-email-and-password"),
        pytest.param(
            {"email": "test@example.com"},
            "Invalid login request",
            id="missing-password",
        ),
        pytest.param(
            {"password": "SomePassword123!"},
            "Invalid login request",
            id="missing-email",
        ),
        pytest.param(
            {"email": "", "password": ""},
            "Invalid login request",
            id="empty-values",
        ),
        pytest.param(
            {"email": "invalid-email", "password": "SomePassword123!"},
            "Unauthorized",
            id="invalid-email-format",
        ),
    ],
)
def test_login_request_validation(
    users_api: UsersApiClient,
    payload: dict[str, str],
    expected_error: str,
) -> None:
    response = users_api.login(payload)

    assert response.status == 401

    body = response.json()
    assert isinstance(body, dict), "Error response must be a JSON object"
    assert body["error"] == expected_error
    assert "access_token" not in body, (
        "Invalid login request must not return an access token"
    )


def test_get_current_user_with_valid_token(
    users_api: UsersApiClient,
    test_user: dict[str, str],
    auth_token: str,
) -> None:
    response = users_api.get_current_user(auth_token)

    assert response.status == 200

    current_user = CurrentUserResponse.model_validate(response.json())
    assert current_user.email == test_user["email"]
    assert current_user.id == test_user["id"]


def test_get_current_user_without_token(users_api: UsersApiClient) -> None:
    response = users_api.get_current_user()

    assert response.status == 401

    body = response.json()
    assert isinstance(body, dict), "Error response must be a JSON object"
    assert body["message"] == "Unauthorized"


def test_get_current_user_with_invalid_token(users_api: UsersApiClient) -> None:
    response = users_api.get_current_user("invalid-token")

    assert response.status == 401

    body = response.json()
    assert isinstance(body, dict), "Error response must be a JSON object"
    assert body["message"] == "Unauthorized"
