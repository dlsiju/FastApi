from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL ="postgresql://postgres:postgres@localhost:5432/postgres"
SQLALCHEMY_DATABASE_URL = DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)