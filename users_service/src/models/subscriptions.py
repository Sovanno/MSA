# файл: users_service/src/models/subscriptions.py
from sqlalchemy import Column, Integer, BigInteger, TIMESTAMP, func, UniqueConstraint
from src.database import base

class Subscriber(base):
    __tablename__ = "subscribers"
    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, nullable=False, index=True)
    author_id = Column(Integer, nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint('subscriber_id', 'author_id', name='ux_sub'),)


class NotificationSent(base):
    __tablename__ = "notifications_sent"
    id = Column(Integer, primary_key=True, index=True)
    subscriber_id = Column(Integer, nullable=False, index=True)
    post_id = Column(Integer, nullable=False, index=True)
    sent_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint('subscriber_id', 'post_id', name='ux_notification'),)
