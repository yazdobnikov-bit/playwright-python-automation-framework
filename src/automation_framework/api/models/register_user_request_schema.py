from pydantic import BaseModel, Field


class RegisterUserRequest(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
