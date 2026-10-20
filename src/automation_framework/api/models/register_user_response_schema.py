from datetime import datetime

from pydantic import BaseModel, Field


class RegisterUserAddress(BaseModel):
    street: str | None
    house_number: str | None
    city: str | None
    state: str | None
    country: str | None
    postal_code: str | None


class RegisterUserResponse(BaseModel):
    id: str = Field(min_length=1)
    email: str = Field(min_length=1)
    first_name: str
    last_name: str
    created_at: datetime
    address: RegisterUserAddress
