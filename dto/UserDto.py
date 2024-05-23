from typing import Union

from pydantic import BaseModel


class UserDto(BaseModel):
    name: str
    age: int
    place: str
    email: str
    Sin_number: str | None = None
    password: str | None = 'defaultPassword'
