import uvicorn
from fastapi import FastAPI

from dto.UserDto import UserDto
from enums.Days import Day

fastapi = FastAPI()


@fastapi.get("/getMessage/{name}/{age}/{day}")
def get_method(name, age: int, day: Day):
    if day is Day.MONDAY:
        return {"response": {"name": name, "age": age, "isHoliday": False, "day": day}}
    else:
        return {"response": {"name": name, "age": age, "isHoliday": True, "days": day}}


@fastapi.post("/")
def post_method():
    return {"response": "called post api"}


@fastapi.delete("/")
def delete_method():
    return {"response": "called delete api"}


@fastapi.put("/")
def put_method():
    return {"response": "called put api"}


@fastapi.post("/file/{fpath:path}")
def path_value(fpath: str):
    return {"response": {"uploadedFile": fpath}}


@fastapi.get("/getlist")
def getWithQueryParam(country: str, pl: str = 'KERALA', ):
    print('country=', country)
    return {"response": {"Place": pl, "country": country}}


@fastapi.post("/user/register")
def register_user(user: UserDto):
    print(user.name)
    print(user.place)
    print(user.age)
    print(user.email)
    print(user.Sin_number)
    return user


if __name__ == "__main__":
    uvicorn.run("main:fastapi", port=8080, log_level="debug")
