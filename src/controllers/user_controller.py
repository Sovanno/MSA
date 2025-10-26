from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src import models

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, email: str, username: str, password: str):
    if db.query(models.user.User).filter(models.user.User.email == email).first():
        raise ValueError("Пользователь с таким email уже существует")
    if db.query(models.user.User).filter(models.user.User.username == username).first():
        raise ValueError("Пользователь с таким username уже существует")

    hashed_pwd = get_password_hash(password)
    user = models.user.User(email=email, username=username, password=hashed_pwd)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.user.User).filter(models.user.User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


def get_user_by_username(db: Session, username: str):
    return db.query(models.user.User).filter(models.user.User.username == username).first()


def update_user(db: Session, user: models.user.User, email: str = None, username: str = None, bio: str = None, image: str = None, password: str = None):
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
    db.commit()
    db.refresh(user)
    return user
