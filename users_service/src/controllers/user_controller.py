from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from src import models
from sqlalchemy import select, and_

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_user(db: AsyncSession, email: str, username: str, password: str):
    # Проверка email
    result = await db.execute(select(models.user.User).where(models.user.User.email == email))
    existing_user = result.scalar_one_or_none()    # <- вот так
    if existing_user:
        raise ValueError("Пользователь с таким email уже существует")

    # Проверка username
    result = await db.execute(select(models.user.User).where(models.user.User.username == username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise ValueError("Пользователь с таким username уже существует")

    hashed_pwd = get_password_hash(password)
    user = models.user.User(email=email, username=username, password=hashed_pwd)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(models.user.User).where(models.user.User.email == email))
    user = result.scalars().first()
    if not user or not verify_password(password, user.password):
        return None
    return user

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.user.User).where(models.user.User.username == username))
    return result.scalars().first()

async def update_user(db: AsyncSession, user: models.user.User, email: str = None, username: str = None, bio: str = None, image: str = None, password: str = None):
    if email is not None:
        user.email = email
    if username is not None:
        user.username = username
    if bio is not None:
        user.bio = bio
    if image is not None:
        user.image = image
    if password is not None:
        user.password = get_password_hash(password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_subscription_key(db: AsyncSession, user: models.user.User, subscription_key: str) -> models.user.User:
    """
    Обновляет subscription_key для пользователя
    """
    user.subscription_key = subscription_key
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def subscribe_to_author(
        db: AsyncSession,
        subscriber_id: int,
        author_id: int
) -> models.subscriber.Subscriber:

    if subscriber_id == author_id:
        raise ValueError("Нельзя подписаться на самого себя")

    author_result = await db.execute(
        select(models.user.User).where(models.user.User.id == author_id)
    )
    author = author_result.scalar_one_or_none()

    if not author:
        raise ValueError(f"Автор с ID {author_id} не найден")

    existing_subscription_result = await db.execute(
        select(models.subscriber.Subscriber).where(
            and_(
                models.subscriber.Subscriber.subscriber_id == subscriber_id,
                models.subscriber.Subscriber.author_id == author_id
            )
        )
    )
    existing_subscription = existing_subscription_result.scalar_one_or_none()

    if existing_subscription:
        raise ValueError("Вы уже подписаны на этого автора")

    subscription = models.subscriber.Subscriber(
        subscriber_id=subscriber_id,
        author_id=author_id
    )

    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)

    return subscription


async def unsubscribe_from_author(
        db: AsyncSession,
        subscriber_id: int,
        author_id: int
) -> bool:
    result = await db.execute(
        select(models.subscriber.Subscriber).where(
            and_(
                models.subscriber.Subscriber.subscriber_id == subscriber_id,
                models.subscriber.Subscriber.author_id == author_id
            )
        )
    )
    subscription = result.scalar_one_or_none()

    if not subscription:
        return False

    await db.delete(subscription)
    await db.commit()

    return True


async def get_subscribers_with_keys(
        db: AsyncSession,
        author_id: int
):
    result = await db.execute(
        select(
            models.user.User.id,
            models.user.User.subscription_key
        ).join(
            models.subscriber.Subscriber,
            models.subscriber.Subscriber.subscriber_id == models.user.User.id
        ).where(
            models.subscriber.Subscriber.author_id == author_id
        )
    )

    subscribers = result.all()

    return [
        {
            "subscriber_id": user_id,
            "subscription_key": subscription_key
        }
        for user_id, subscription_key in subscribers
    ]


async def get_user_subscriptions(
        db: AsyncSession,
        user_id: int
):
    result = await db.execute(
        select(models.user.User).join(
            models.subscriber.Subscriber,
            models.subscriber.Subscriber.author_id == models.user.User.id
        ).where(
            models.subscriber.Subscriber.subscriber_id == user_id
        )
    )

    return result.scalars().all()


async def is_subscribed(
        db: AsyncSession,
        subscriber_id: int,
        author_id: int
) -> bool:

    result = await db.execute(
        select(models.subscriber.Subscriber).where(
            and_(
                models.subscriber.Subscriber.subscriber_id == subscriber_id,
                models.subscriber.Subscriber.author_id == author_id
            )
        )
    )

    subscription = result.scalar_one_or_none()
    return subscription is not None
