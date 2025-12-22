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
    subscription_key = Column(String, nullable=True)

    subscriptions = relationship(
        "Subscriber",
        foreign_keys="Subscriber.subscriber_id",
        back_populates="subscriber",
        cascade="all, delete-orphan", passive_deletes=True
    )

    subscribers = relationship(
        "Subscriber",
        foreign_keys="Subscriber.author_id",
        back_populates="author",
        cascade="all, delete-orphan", passive_deletes=True
    )
