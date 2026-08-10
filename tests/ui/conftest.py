import pytest
from playwright.sync_api import Page

from automation_framework.ui.pages_container import Pages


@pytest.fixture
def pages(page: Page) -> Pages:
    return Pages(page)
