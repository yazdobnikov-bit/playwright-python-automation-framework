import pytest

from automation_framework.api.clients.products_client import ProductsClient
from automation_framework.api.models.product_schema import ProductSchema
from automation_framework.api.models.products_response_schema import (
    ProductsResponseSchema,
)
from automation_framework.api.models.search_product_schema import (
    SearchProductsResponseSchema,
)


def test_get_products(products_client: ProductsClient):
    response = products_client.get_products()

    assert response.status == 200

    products_response = ProductsResponseSchema.model_validate(response.json())
    assert products_response.data, "No products found in the response"


def test_get_product_by_id(products_client: ProductsClient):
    products_response = products_client.get_products()
    product_id = products_response.json()["data"][0]["id"]
    response = products_client.get_product(product_id)
    body = response.json()
    product = ProductSchema.model_validate(body)

    assert response.status == 200
    assert product.id == product_id
    assert product.category.name
    assert product.brand.name


def test_get_non_existing_product(products_client: ProductsClient):
    response = products_client.get_product("nonexistent_id")
    assert response.status == 404
    assert response.json()["message"] == "Requested item not found"


@pytest.mark.parametrize("search_query", ["Hammer", "Pliers", "Saw"])
def test_search_products(products_client: ProductsClient, search_query: str):
    response = products_client.search_products(search_query)

    assert response.status == 200

    products_response = SearchProductsResponseSchema.model_validate(response.json())
    assert products_response.data, "No products found in the response"

    for product in products_response.data:
        assert search_query.lower() in product.name.lower(), (
            f"Product '{product.name}' does not contain '{search_query}'"
        )
