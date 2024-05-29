import uuid

from pydantic import BaseModel

class AddressDetails(BaseModel):
    id: uuid.UUID | None = None
    user_id: uuid.UUID | None = None
    country: str
    street: str
    zip_code: str
    phone: str

class UserDetail(BaseModel):
    id: uuid.UUID | None = None
    name: str
    age: str
    place: str
    email: str
    address: AddressDetails

    class Config:
        orm_mode = True



