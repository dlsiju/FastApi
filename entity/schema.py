from pydantic import BaseModel


class UserDetail(BaseModel):
    id: int
    name: str
    age: str
    place: str

    class Config:
        orm_mode = True
