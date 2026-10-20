from typing import Literal

from pydantic import BaseModel, Field, StrictInt


class LoginResponse(BaseModel):
    access_token: str = Field(min_length=1)
    token_type: Literal["bearer"]
    expires_in: StrictInt = Field(gt=0)
