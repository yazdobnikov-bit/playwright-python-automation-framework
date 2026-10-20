from pydantic import BaseModel


class CurrentUserAddress(BaseModel):
    street: str | None
    house_number: str | None
    city: str | None
    state: str | None
    country: str | None
    postal_code: str | None


class CurrentUserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone: str | None
    dob: str | None
    email: str
    totp_enabled: bool
    created_at: str
    address: CurrentUserAddress
