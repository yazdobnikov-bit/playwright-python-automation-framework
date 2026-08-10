from playwright.sync_api import Locator


class ProductCard:
    def __init__(self, root: Locator):
        self.root = root
        self.name = self.root.locator('[data-test="product-name"]')
        self.price = self.root.locator('[data-test="product-price"]')
        self.compare_btn = self.root.locator('[data-test="compare-btn"]')
