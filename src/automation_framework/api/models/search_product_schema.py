from pydantic import BaseModel

from automation_framework.api.models.product_schema import BrandSchema


class SearchCategorySchema(BaseModel):
    id: str
    name: str


class SearchProductSchema(BaseModel):
    id: str
    name: str
    price: float
    category: SearchCategorySchema
    brand: BrandSchema


class SearchProductsResponseSchema(BaseModel):
    data: list[SearchProductSchema]
    current_page: int
    total: int
