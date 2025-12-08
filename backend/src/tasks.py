from .celery_app import celery_app
import requests
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="notify_followers", max_retries=3)
def notify_followers_task(self, author_id: int, article_slug: str):

    task_id = self.request.id
    logger.info(f"Starting notification task {task_id} for author {author_id}, article {article_slug}")

    try:
        backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")
        article_response = requests.get(f"{backend_url}/api/articles/{article_slug}")

        if article_response.status_code != 200:
            error_msg = f"Article not found: {article_slug}"
            logger.error(error_msg)
            raise Exception(error_msg)

        article_data = article_response.json()
        title = article_data.get("title", "New article")
        short_title = (title[:10] + "...") if len(title) > 10 else title

        users_service_url = os.environ.get("USERS_SERVICE_URL", "http://localhost:8001")
        subscribers_response = requests.get(
            f"{users_service_url}/api/users/{author_id}/subscribers"
        )

        if subscribers_response.status_code != 200:
            error_msg = f"Failed to get subscribers for author {author_id}"
            logger.error(error_msg)
            raise Exception(error_msg)

        subscribers_data = subscribers_response.json()
        subscribers = subscribers_data.get("subscribers", [])

        if not subscribers:
            logger.warning(f"No subscribers found for author {author_id}")
            return {
                "task_id": task_id,
                "status": "no_subscribers",
                "author_id": author_id,
                "article_slug": article_slug
            }

        push_service_url = os.environ.get("PUSH_SERVICE_URL", "http://push-notificator:8000/api/v1/notify")
        successful_sends = 0
        skipped_no_key = 0
        errors = 0

        for subscriber in subscribers:
            subscriber_id = subscriber.get("subscriber_id")
            subscription_key = subscriber.get("subscription_key")

            if not subscription_key:
                logger.warning(f"Skipping subscriber {subscriber_id}: no subscription key")
                skipped_no_key += 1
                continue

            message = f"Пользователь {author_id} выпустил новый пост: {short_title}"

            try:
                response = requests.post(
                    push_service_url,
                    headers={
                        "Authorization": f"Bearer {subscription_key}",
                        "Content-Type": "application/json"
                    },
                    json={"message": message},
                    timeout=5
                )
                response.raise_for_status()
                successful_sends += 1
                logger.info(f"Notification sent to subscriber {subscriber_id}")
            except requests.RequestException as e:
                logger.error(f"Failed to send notification to subscriber {subscriber_id}: {str(e)}")
                errors += 1
                continue

        logger.info(
            f"Task {task_id} completed. "
            f"Successful: {successful_sends}, "
            f"Skipped (no key): {skipped_no_key}, "
            f"Errors: {errors}"
        )

        return {
            "task_id": task_id,
            "status": "completed",
            "successful_sends": successful_sends,
            "skipped_no_key": skipped_no_key,
            "errors": errors,
            "author_id": author_id,
            "article_slug": article_slug,
            "total_subscribers": len(subscribers)
        }

    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}")
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
