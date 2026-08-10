from playwright.sync_api import Page

from automation_framework.ui.components.search import Search


class Filters:
    def __init__(self, page: Page):
        self.page = page
        self.filters = self.page.locator('[data-test="filters"]')
        self.search = Search(self.filters)
