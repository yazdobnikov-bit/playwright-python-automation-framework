from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: str
    name: str
    slug: str


class BrandSchema(BaseModel):
    id: str
    name: str


class ProductSchema(BaseModel):
    id: str
    name: str
    price: float
    category: CategorySchema
    brand: BrandSchema
