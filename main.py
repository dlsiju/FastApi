import uuid
from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
import uvicorn
from fastapi import FastAPI, Query, Path, Depends, HTTPException, status,Request
from fastapi.params import Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import and_

from Middleware import Middleware
from dto.Location import Location
from dto.LoginDto import LoginDto
from dto.UserDto import UserDto
from enums.Days import Day
from entity.models import User, Address, Account, Login
from sqlalchemy.orm import Session
from DbConfiguration.ConnectDb import SessionLocal
from entity.schema import UserDetail, UserAuth, LoggedInResult, AppResponse

fastapi = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_token")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


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
def create_user(usr: UserDetail, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    print('name=', usr.name)
    print('age=', usr.age)
    print('email=', usr.email)
    print('country=', usr.address.country)
    print('street=', usr.address.street)
    print('zipcode=', usr.address.zip_code)
    saved_user = save_user(db, usr)
    return saved_user


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
    bank_accounts = []
    for acc in usr.account:
        account = Account()
        account.id = uuid.uuid4()
        account.bank = acc.name
        account.balance = acc.balance
        bank_accounts.append(account)
    user.accounts = bank_accounts
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


@fastapi.post("/login_token")
async def auth_user(loginForm: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db)):
    print('calledddddddddddddddddd auth_user')
    print('useranem=', loginForm.username)
    print('password=', loginForm.password)
    login = db_session.query(Login).filter(
        and_(Login.username == loginForm.username, Login.password == loginForm.password)).first()
    if not login:
       return AppResponse(status="success",data="Username or password is incorrect")
    else:
        print('login found')
        print('login userId=', login.user_id)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        generated_jwt_token = generate_jwt_token(login.username, access_token_expires)
        print('access_token_expires=', access_token_expires)
        return LoggedInResult(token=generated_jwt_token, token_type="bearer")


def generate_jwt_token(user_name: str, expireTime: timedelta):
    expire = datetime.now(timezone.utc) + expireTime
    data = {"sub": user_name}.copy()
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    return username


async def get_current_active_user(
        current_user: Annotated[str, Depends(get_current_user)],
):
    return current_user


@fastapi.get("/users/me/")
async def get_logged_in(
        current_user: Annotated[str, Depends(get_current_active_user)],
):
    return current_user


if __name__ == "__main__":
    uvicorn.run("main:fastapi", port=8080, log_level="debug")
