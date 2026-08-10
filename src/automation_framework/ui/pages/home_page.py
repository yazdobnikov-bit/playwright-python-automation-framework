from playwright.sync_api import Page

from automation_framework.ui.components.product_grid import ProductGrid
from automation_framework.ui.pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page, path="/")
        self.products = ProductGrid(self.page)
