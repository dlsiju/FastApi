

from sqlalchemy import Column, String, Uuid
from DbConfiguration.ConnectDb import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Uuid,primary_key=True)
    name = Column(String, unique=True, index=True)
    age = Column(String, default=True)
    place = Column(String, default=True)
