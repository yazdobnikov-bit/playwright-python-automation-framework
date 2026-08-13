import tomllib

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from automation_framework.api.clients.products_client import ProductsClient


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
