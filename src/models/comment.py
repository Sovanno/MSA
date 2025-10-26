from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database import base
from datetime import datetime


class Comment(base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    article = relationship("Article", back_populates="comments")
    author = relationship("User", back_populates="comments")
