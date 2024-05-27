from pydantic import BaseModel, Field


class Location(BaseModel):
    country: str
    country_phone_code: str = Field(description='country_phone_code must be present',min_length=20)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tags: list[str] = []

