from playwright.sync_api import Page

from automation_framework.ui.components.categories import Categories
from automation_framework.ui.components.search import Search


class Filters:
    def __init__(self, page: Page):
        self.page = page
        self.root = self.page.locator('[data-test="filters"]')
        self.search = Search(self.root)
        self.categories = Categories(self.root)
