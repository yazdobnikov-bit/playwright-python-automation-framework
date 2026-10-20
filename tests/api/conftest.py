import tomllib
from collections.abc import Callable

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from automation_framework.api.clients.products_client import ProductsClient
from automation_framework.api.clients.users_api_client import UsersApiClient
from automation_framework.api.data.user_factory import build_register_user
from automation_framework.api.models.login_response_schema import LoginResponse


@pytest.fixture
def api_base_url(pytestconfig) -> str:
    config_path = pytestconfig.rootpath / "pyproject.toml"

    with config_path.open("rb") as file:
        config = tomllib.load(file)

    return config["tool"]["automation_framework"]["api_base_url"]


@pytest.fixture
def api_request_context(
    playwright: Playwright,
    api_base_url: str,
) -> APIRequestContext:
    context = playwright.request.new_context(
        base_url=api_base_url,
    )

    yield context

    context.dispose()


@pytest.fixture
def products_client(api_request_context: APIRequestContext) -> ProductsClient:
    return ProductsClient(api_request_context)


@pytest.fixture
def users_api(api_request_context: APIRequestContext) -> UsersApiClient:
    return UsersApiClient(api_request_context)


@pytest.fixture
def user_factory(
    users_api: UsersApiClient,
) -> Callable[..., dict[str, str]]:
    def create_user(
        first_name: str = "Test",
        last_name: str = "User",
    ) -> dict[str, str]:
        request_model = build_register_user(first_name, last_name)
        response = users_api.register(request_model.model_dump())

        if response.status != 201:
            raise RuntimeError(f"Failed to create test user: HTTP {response.status}")

        body = response.json()
        user_id = body.get("id") if isinstance(body, dict) else None
        if not isinstance(user_id, str) or not user_id:
            raise RuntimeError("Failed to create test user: invalid user ID")

        return {
            "id": user_id,
            "email": request_model.email,
            "password": request_model.password,
        }

    return create_user


@pytest.fixture(scope="function")
def test_user(user_factory: Callable[..., dict[str, str]]) -> dict[str, str]:
    return user_factory()


@pytest.fixture(scope="function")
def auth_token(
    users_api: UsersApiClient,
    test_user: dict[str, str],
) -> str:
    response = users_api.login(
        {"email": test_user["email"], "password": test_user["password"]},
    )

    assert response.status == 200, f"Login failed: expected 200, got {response.status}"

    login_response = LoginResponse.model_validate(response.json())
    return login_response.access_token


@pytest.fixture(scope="function")
def second_user(
    users_api: UsersApiClient,
    user_factory: Callable[..., dict[str, str]],
) -> dict[str, str]:
    user = user_factory()
    login_response = users_api.login(
        {"email": user["email"], "password": user["password"]},
    )

    assert login_response.status == 200

    login = LoginResponse.model_validate(login_response.json())
    return {
        "id": user["id"],
        "email": user["email"],
        "token": login.access_token,
    }
