from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from src import models
from sqlalchemy import select, update, delete

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_user(db: AsyncSession, email: str, username: str, password: str):
    result = await db.execute(select(models.user.User).filter(models.user.User.email == email))
    if result.scalar_one_or_none():
        raise ValueError("Пользователь с таким email уже существует")

    # Проверяем, существует ли username
    result = await db.execute(select(models.user.User).filter(models.user.User.username == username))
    if result.scalar_one_or_none():
        raise ValueError("Пользователь с таким username уже существует")

    hashed_pwd = get_password_hash(password)
    user = models.user.User(email=email, username=username, password=hashed_pwd)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(models.user.User).filter(models.user.User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password):
        return None
    return user


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.user.User).filter(models.user.User.username == username))
    return result.scalar_one_or_none()


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
    await db.commit()
    await db.refresh(user)
    return user
