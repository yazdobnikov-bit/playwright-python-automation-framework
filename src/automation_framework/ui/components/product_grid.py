from playwright.sync_api import Locator, Page

from automation_framework.ui.components.product_card import ProductCard


class ProductGrid:
    def __init__(self, page: Page):
        self.page = page
        self.products = page.locator('[data-test^="product-"]')
        self.result_count = self.page.locator('[data-test="search-result-count"]')
        self.product_names = self.products.locator('[data-test="product-name"]')
        self.filter_completed = self.page.locator('[data-test="filter_completed"]')
        self.search_completed = self.page.locator('[data-test="search_completed"]')

    def get_first_product(self) -> ProductCard:
        return ProductCard(self.products.first)

    def get_product_by_name(self, name: str) -> ProductCard:
        product_name = self.page.locator('[data-test="product-name"]').filter(
            has_text=name
        )
        return ProductCard(self.products.filter(has=product_name))

    def get_product_names(self) -> Locator:
        return self.product_names

    def get_all_products(self) -> list[ProductCard]:
        return [ProductCard(product) for product in self.products.all()]
