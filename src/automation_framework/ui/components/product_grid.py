from playwright.sync_api import Page

from automation_framework.ui.components.product_card import ProductCard


class ProductGrid:
    def __init__(self, page: Page):
        self.page = page
        self.products = page.locator('[data-test^="product-"]')

    def get_first_product(self) -> ProductCard:
        return ProductCard(self.products.first)

    def get_product_by_name(self, name: str) -> ProductCard:
        product_name = self.page.locator('[data-test="product-name"]').filter(
            has_text=name
        )
        return ProductCard(self.products.filter(has=product_name))
