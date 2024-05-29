

from sqlalchemy import Column, String, Uuid, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Uuid,primary_key=True)
    name = Column(String, unique=True, index=True)
    age = Column(String, default=True)
    place = Column(String, default=True)
    email = Column(String, unique=True, index=True)
    address = relationship("Address", uselist=False, back_populates="parent")


class Address(Base):
    __tablename__ = "address"
    id = Column(Uuid, primary_key=True)
    user_id = Column(Uuid, ForeignKey("user.id"), nullable=False)
    country = Column(String, unique=True, index=True)
    street = Column(String, unique=True, index=True)
    zip_code = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    parent = relationship("User", back_populates="address")
