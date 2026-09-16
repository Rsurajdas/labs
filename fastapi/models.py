from database import Base
from sqlalchemy import Column, Integer, String, Text, CheckConstraint

class Books(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    description = Column(Text)
    author = Column(String(50), nullable=False)
    rating = Column(Integer, CheckConstraint("rating >= 1 AND rating <= 5"))