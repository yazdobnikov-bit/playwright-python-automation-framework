import pytest

from automation_framework.api.clients.users_api_client import UsersApiClient
from automation_framework.api.models.current_user_response_schema import (
    CurrentUserResponse,
)


def test_update_current_user_first_name(
    users_api: UsersApiClient,
    test_user: dict[str, str],
    auth_token: str,
) -> None:
    update_response = users_api.update_user(
        test_user["id"],
        {"first_name": "Updated"},
        auth_token,
    )

    assert update_response.status == 200
    assert update_response.json()["success"] is True

    get_response = users_api.get_current_user(auth_token)

    assert get_response.status == 200

    current_user = CurrentUserResponse.model_validate(get_response.json())
    assert current_user.first_name == "Updated"
    assert current_user.id == test_user["id"]
    assert current_user.email == test_user["email"]
    assert current_user.last_name == "User"


def test_user_can_read_own_profile_by_id(
    users_api: UsersApiClient,
    test_user: dict[str, str],
    auth_token: str,
) -> None:
    get_response = users_api.get_user_by_id(test_user["id"], auth_token)

    assert get_response.status == 200

    current_user = CurrentUserResponse.model_validate(get_response.json())
    assert current_user.id == test_user["id"]
    assert current_user.email == test_user["email"]


def test_user_cannot_read_another_user_profile(
    users_api: UsersApiClient,
    test_user: dict[str, str],
    auth_token: str,
    second_user: dict[str, str],
) -> None:
    user_b_id = second_user["id"]
    assert user_b_id != test_user["id"]

    get_response = users_api.get_user_by_id(user_b_id, auth_token)

    assert get_response.status == 404

    body = get_response.json()
    assert body["error"] == "You are not authorized to view this user."
    assert "email" not in body
    assert "first_name" not in body
    assert "id" not in body


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(None, id="missing-token"),
        pytest.param("invalid-token", id="invalid-token"),
    ],
)
def test_get_user_by_id_without_valid_authentication(
    users_api: UsersApiClient,
    test_user: dict[str, str],
    token: str | None,
) -> None:
    get_response = users_api.get_user_by_id(test_user["id"], token)

    assert get_response.status == 401
    assert get_response.json()["message"] == "Unauthorized"


def test_user_cannot_update_another_user_profile(
    users_api: UsersApiClient,
    test_user: dict[str, str],
    auth_token: str,
    second_user: dict[str, str],
) -> None:
    user_b_id = second_user["id"]
    token_b = second_user["token"]
    assert user_b_id != test_user["id"]
    original_response = users_api.get_current_user(token_b)

    assert original_response.status == 200

    original_user_b = CurrentUserResponse.model_validate(original_response.json())
    assert original_user_b.id == user_b_id
    assert original_user_b.email == second_user["email"]

    update_response = users_api.update_user(
        user_b_id,
        {"first_name": "Hacked"},
        auth_token,
    )

    assert update_response.status == 403
    assert update_response.json()["error"] == "You can only update your own data."

    get_response = users_api.get_current_user(token_b)

    assert get_response.status == 200

    updated_user_b = CurrentUserResponse.model_validate(get_response.json())
    assert updated_user_b == original_user_b


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(None, id="missing-token"),
        pytest.param("invalid-token", id="invalid-token"),
    ],
)
def test_update_user_without_valid_authentication(
    users_api: UsersApiClient,
    test_user: dict[str, str],
    auth_token: str,
    token: str | None,
) -> None:
    update_response = users_api.update_user(
        test_user["id"],
        {"first_name": "UnauthorizedUpdate"},
        token,
    )

    assert update_response.status == 401
    assert update_response.json()["message"] == "Unauthorized"

    get_response = users_api.get_current_user(auth_token)

    assert get_response.status == 200

    current_user = CurrentUserResponse.model_validate(get_response.json())
    assert current_user.first_name == "Test"
    assert current_user.id == test_user["id"]
    assert current_user.email == test_user["email"]
