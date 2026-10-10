from database import Base
from sqlalchemy import Column, Integer, String, Text, Boolean


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(Text)
    priority = Column(Integer, nullable=False)
    complete = Column(Boolean, default=False)
