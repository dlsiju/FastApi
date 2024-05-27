import uuid

from pydantic import BaseModel


class UserDetail(BaseModel):
    user_id: uuid.UUID | None = None
    name: str
    age: str
    place: str

    class Config:
        orm_mode = True
