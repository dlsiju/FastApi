from sqlalchemy import Column, Uuid, String

from DbConfiguration.ConnectDb import Base


class Address(Base):
    __tablename__ = "user_address"

    address_id = Column(Uuid, primary_key=True)
    house_number = Column(String, unique=True, index=True)
    city = Column(String, default=True)
    state = Column(String, default=True)
    country = Column(String, default=True)