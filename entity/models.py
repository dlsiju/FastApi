from sqlalchemy import Column, String, Uuid, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Uuid, primary_key=True)
    name = Column(String, index=True)
    age = Column(String, default=True)
    place = Column(String, default=True)
    email = Column(String, unique=True, index=True)
    address = relationship("Address", uselist=False, back_populates="parent", cascade="all, delete")
    accounts = relationship("Account", uselist=True, back_populates="accountUser", cascade="all, delete")


class Address(Base):
    __tablename__ = "address"
    id = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, ForeignKey("user.id"), nullable=False)
    country = Column(String, index=True)
    street = Column(String, index=True)
    zip_code = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    parent = relationship("User", back_populates="address")


class Account(Base):
    __tablename__ = "account"
    id = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, ForeignKey("user.id"), nullable=False)
    bank = Column(String, index=True)
    balance = Column(String, index=True)
    accountUser = relationship("User", back_populates="accounts")
