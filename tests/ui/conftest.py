import pytest
from playwright.sync_api import Page

from automation_framework.ui.pages_container import Pages


@pytest.fixture
def pages(page: Page) -> Pages:
    return Pages(page)


@pytest.fixture
def browser_context_args(browser_context_args, request):
    device = request.config.getoption("--device")

    if device:
        return browser_context_args

    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
    }
