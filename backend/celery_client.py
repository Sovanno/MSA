from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery = Celery("backend_client", broker=REDIS_URL)

def enqueue_notify(author_id: int, post_id: int):
    celery.send_task("worker.tasks.notify_followers", args=[author_id, post_id], kwargs={})
