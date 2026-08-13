from playwright.sync_api import APIRequestContext, APIResponse


class ProductsClient:
    def __init__(self, api_context: APIRequestContext):
        self.api_context = api_context

    def get_products(self) -> APIResponse:
        return self.api_context.get("/products")

    def get_product(self, product_id: str) -> APIResponse:
        return self.api_context.get(f"/products/{product_id}")

    def search_products(self, query: str) -> APIResponse:
        return self.api_context.get("/products/search", params={"q": query})
