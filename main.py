from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query, Path, Depends
from fastapi.params import Body

from dto.Location import Location
from dto.LoginDto import LoginDto
from dto.UserDto import UserDto
from enums.Days import Day
from entity.User import User
from sqlalchemy.orm import Session
from DbConfiguration.ConnectDb import SessionLocal
from entity.schema import UserDetail

fastapi = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@fastapi.get("/getMessage/{name}/{age}/{day}")
def get_method(name, age: Annotated[int, Path(gt=20)], day: Day):
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
    user_dict = user.dict()
    print(list(user_dict.values()))
    return user


@fastapi.patch("/user/update/{uid}")
def get_user_by_name_and_email(user: UserDto, sin: str, uid: str):
    return {"response": {"user": {"uid": uid, "sin": sin, "details": {"name": user.name}}}}


@fastapi.get("/param/validate")
def param_with_validation(num: Annotated[int | None, Query(gt=47)] = None):
    return {"response": {"num": num}}


@fastapi.post("/login")
def login(logindto: LoginDto, location: Location, dobd: Annotated[str, Body()]):
    print('username=' + logindto.username)
    print('password=' + logindto.password)
    print('country=', location.country)
    print("countryCode=" + location.country_phone_code)


@fastapi.post("/location/save")
def saveLocation(location: Annotated[Location, Body(embed=True)]):
    print('country=', location.country)
    print('country_code=', location.country_phone_code)
    print('list=', location.tags)


@fastapi.post("/dic/")
async def create_index_weights(weights: dict[int, float]):
    return weights


@fastapi.post('/create/', response_model=UserDetail)
def create_user(usr: UserDetail, db: Session = Depends(get_db)):
    db_place = save_user(db, usr)
    return db_place


def save_user(db: Session, usr: User):
    db_place = User(**usr.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


@fastapi.get("/getAllUsers", response_model=list[UserDetail])
def get_all_users(db_session: Session = Depends(get_db)):
    return db_session.query(User)


@fastapi.get("/getUserById", response_model=UserDetail)
def get_user_by_id(userId: int, db_session: Session = Depends(get_db)):
    return db_session.get(User, userId)


@fastapi.get("/getUserByPlace", response_model=list[UserDetail])
def get_user_by_place(plc: str, db_session: Session = Depends(get_db)):
    return db_session.query(User).filter(User.place == plc)


if __name__ == "__main__":
    uvicorn.run("main:fastapi", port=8080, log_level="debug")
