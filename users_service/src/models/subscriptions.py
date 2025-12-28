# users_service/src/models/subscriptions.py
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, UniqueConstraint
from sqlalchemy.orm import relationship
from src.database import base


class Subscriber(base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True, index=True)

    subscriber_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    subscriber_user = relationship(
        "User",
        foreign_keys=[subscriber_id],
        back_populates="subscriptions"
    )

    author_user = relationship(
        "User",
        foreign_keys=[author_id],
        back_populates="subscribers"
    )

    __table_args__ = (UniqueConstraint('subscriber_id', 'author_id', name='ux_sub'),)


class NotificationSent(base):
    __tablename__ = "notifications_sent"
    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, nullable=False, index=True)
    post_id = Column(Integer, nullable=False, index=True)
    sent_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint('subscriber_id', 'post_id', name='ux_notification'),)