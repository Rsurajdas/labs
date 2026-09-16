from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_CONNECTION_URL = "postgresql+psycopg://postgres:suraj123@localhost:5432/books"

engine = create_engine(DATABASE_CONNECTION_URL)

session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()