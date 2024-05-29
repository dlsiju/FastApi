import os
import uuid
from typing import Annotated

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Path, Depends
from fastapi.params import Body
from fastapi.security import OAuth2PasswordBearer

from dto.Location import Location
from dto.LoginDto import LoginDto
from dto.UserDto import UserDto
from enums.Days import Day
from entity.models import User, Address
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
    print('name=', usr.name)
    print('age=', usr.age)
    print('email=', usr.email)
    print('country=', usr.address.country)
    print('street=', usr.address.street)
    print('zipcode=', usr.address.zip_code)
    db_place = save_user(db, usr)
    return db_place


def save_user(db: Session, usr: UserDetail):
    user = User()
    user.name = usr.name
    user.age = usr.age
    user.email = usr.email
    user.place = usr.place
    addr = Address()
    addr.country = usr.address.country
    addr.street = usr.address.street
    addr.zip_code = usr.address.zip_code
    addr.phone = usr.address.phone
    user.id = uuid.uuid4()
    addr.id = uuid.uuid4()
    user.address = addr
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@fastapi.get("/getAllUsers", response_model=list[UserDetail])
def get_all_users(db_session: Session = Depends(get_db)):
    return db_session.query(User)


@fastapi.get("/getUserById", response_model=None)
def get_user_by_id(userId: uuid.UUID, db_session: Session = Depends(get_db)):
    user = db_session.get(User, userId)
    if user is None:
        return {"response": {"message": "user not found"}}
    else:
        return user


@fastapi.get("/getUserByPlace", response_model=list[UserDetail])
def get_user_by_place(plc: str, db_session: Session = Depends(get_db)):
    return db_session.query(User).filter(User.place == plc)


@fastapi.delete("/deleteById")
def delete_by_id(userId: uuid.UUID, db_session: Session = Depends(get_db)):
    user = db_session.get(User, userId)
    if user is None:
        return {"response": {"message": "user not found"}}
    db_session.delete(user)
    db_session.commit()
    return {"response": {"message": "Successfully deleted user"}}


@fastapi.patch("/update")
def update_user(usr: UserDetail, db_session: Session = Depends(get_db)):
    user = db_session.get(User, usr.user_id)
    if user is None:
        return {"response": {"message": "user not found"}}
    user.place = usr.place
    user.name = usr.name
    user.age = usr.age
    db_session.commit()
    return {"response": {"message": "Successfully updated user"}}


if __name__ == "__main__":
    uvicorn.run("main:fastapi", port=8080, log_level="debug")
