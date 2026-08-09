from playwright.sync_api import Page

from automation_framework.ui.components.product_grid import ProductGrid


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.products = ProductGrid(self.page)

    def open(self) -> None:
        self.page.goto('https://practicesoftwaretesting.com')



