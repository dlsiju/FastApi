from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from DbConfiguration.ConnectDb import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    age = Column(String, default=True)
    place = Column(String, default=True)