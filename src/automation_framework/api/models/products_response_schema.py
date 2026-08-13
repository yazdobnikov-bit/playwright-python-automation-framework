from pydantic import BaseModel

from automation_framework.api.models.product_schema import ProductSchema


class ProductsResponseSchema(BaseModel):
    data: list[ProductSchema]
    current_page: int
    total: int
