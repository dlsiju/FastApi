import uuid

from pydantic import BaseModel


class AddressDetails(BaseModel):
    id: uuid.UUID | None = None
    user_id: uuid.UUID | None = None
    country: str
    street: str
    zip_code: str
    phone: str

    class Config:
        orm_mode = True


class AccDetail(BaseModel):
    id: uuid.UUID | None = None
    name: str
    balance: int

    class Config:
        orm_mode = True


class UserDetail(BaseModel):
    id: uuid.UUID | None = None
    name: str
    age: str
    place: str
    email: str
    address: AddressDetails
    account: list[AccDetail]

    class Config:
        orm_mode = True
