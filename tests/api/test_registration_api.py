import pytest

from automation_framework.api.clients.users_api_client import UsersApiClient
from automation_framework.api.data.user_factory import build_register_user
from automation_framework.api.models.register_user_response_schema import (
    RegisterUserResponse,
)
from automation_framework.api.models.registration_error_schema import (
    RegistrationErrorResponse,
)


def test_register_with_valid_data(users_api: UsersApiClient) -> None:
    request_model = build_register_user()
    response = users_api.register(request_model.model_dump())

    assert response.status == 201

    body = response.json()
    assert "password" not in body, "Registration response must not contain password"
    registered_user = RegisterUserResponse.model_validate(body)
    assert registered_user.email == request_model.email


@pytest.mark.parametrize(
    "missing_field",
    [
        pytest.param("email", id="missing-email"),
        pytest.param("password", id="missing-password"),
    ],
)
def test_register_without_required_field(
    users_api: UsersApiClient,
    missing_field: str,
) -> None:
    payload = build_register_user().model_dump()
    payload.pop(missing_field)

    response = users_api.register(payload)

    assert response.status == 422

    error_response = RegistrationErrorResponse.model_validate(response.json())
    assert error_response.root[missing_field] == [
        f"The {missing_field} field is required."
    ]


def test_register_with_multiple_missing_fields(
    users_api: UsersApiClient,
) -> None:
    payload = build_register_user().model_dump()
    payload.pop("email")
    payload.pop("password")

    response = users_api.register(payload)

    assert response.status == 422

    error_response = RegistrationErrorResponse.model_validate(response.json())
    assert error_response.root["email"] == ["The email field is required."]
    assert error_response.root["password"] == ["The password field is required."]


def test_register_with_duplicate_email(
    users_api: UsersApiClient,
    test_user: dict[str, str],
) -> None:
    payload = build_register_user().model_dump()
    payload["email"] = test_user["email"]

    response = users_api.register(payload)

    assert response.status == 409

    error_response = RegistrationErrorResponse.model_validate(response.json())
    assert error_response.root["email"] == [
        "A customer with this email address already exists."
    ]
