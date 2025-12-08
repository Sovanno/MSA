from sqlalchemy import Column, Integer, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from src.database import base


class Subscriber(base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, nullable=False)
    author_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('subscriber_id', 'author_id', name='ux_subscriber_author'),
    )

    subscriber = relationship(
        "User",
        foreign_keys=[subscriber_id],
        back_populates="subscriptions",
        cascade="all, delete-orphan", passive_deletes=True
    )

    author = relationship(
        "User",
        foreign_keys=[author_id],
        back_populates="subscribers",
        cascade="all, delete-orphan", passive_deletes=True
    )
