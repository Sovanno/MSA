from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import base


class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    bio = Column(String, default="")
    image = Column(String, default="")

    articles = relationship("Article", back_populates="author", cascade="all, delete-orphan", passive_deletes=True)
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
