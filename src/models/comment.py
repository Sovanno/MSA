from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database import base
from datetime import datetime

class Comment(base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    article_id = Column(Integer, ForeignKey("aricles.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    article = relationship("Article", back_populates="comments")
    author = relationship("User", back_populates="comments")
