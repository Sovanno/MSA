from celery import Celery
import requests
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from config import settings
from .celery_app import celery_app

REDIS_URL = settings.redis_url
celery = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

USERS_DATABASE_URL = settings.database_users_url.replace(
    "postgresql+asyncpg://",
    "postgresql://"
)
engine = create_engine(USERS_DATABASE_URL, pool_pre_ping=True)

PUSH_URL = settings.push_url
REQUEST_TIMEOUT = 5

@celery_app.task(bind=True, max_retries=5)
def notify_followers(self, author_id: int, post_id: int):

    print(author_id, post_id)
    logging.info("task start: author=%s post=%s", author_id, post_id)
    conn = engine.connect()
    try:
        sql = text("""
            SELECT s.subscriber_id, u.subscription_key
            FROM subscribers s
            LEFT JOIN users u ON u.id = s.subscriber_id
            WHERE s.author_id = :author_id
        """)
        rows = conn.execute(sql, {"author_id": author_id}).fetchall()

        for row in rows:
            subscriber_id = row[0]
            subscription_key = row[1]
            if not subscription_key:
                logging.warning("Subscriber %s has no subscription_key, skip", subscriber_id)
                continue

            try:
                insert_sql = text("INSERT INTO notifications_sent (subscriber_id, post_id) VALUES (:sid, :pid)")
                conn.execute(insert_sql, {"sid": subscriber_id, "pid": post_id})
                conn.commit()
            except IntegrityError:
                conn.rollback()
                logging.info("Notification already sent to %s for post %s, skip", subscriber_id, post_id)
                continue
            except Exception as e:
                conn.rollback()
                logging.error("DB error when creating notifications_sent: %s", e)
                raise self.retry(exc=e, countdown=2 ** self.request.retries)

            msg = f"Пользователь {author_id} выпустил новый пост: {str(post_id)[:10]}"

            headers = {
                "Authorization": f"Bearer {subscription_key}",
                "Content-Type": "application/json",
            }
            try:
                r = requests.post(PUSH_URL, headers=headers, json={"message": msg}, timeout=REQUEST_TIMEOUT)
                r.raise_for_status()
                logging.info("Push sent to %s status=%s", subscriber_id, r.status_code)
            except requests.RequestException as exc:
                logging.error("Push failed for subscriber %s: %s", subscriber_id, exc)
                try:
                    del_sql = text("DELETE FROM notifications_sent WHERE subscriber_id = :sid AND post_id = :pid")
                    conn.execute(del_sql, {"sid": subscriber_id, "pid": post_id})
                    conn.commit()
                except Exception:
                    conn.rollback()
                raise self.retry(exc=exc, countdown=2 ** self.request.retries)

    finally:
        conn.close()
