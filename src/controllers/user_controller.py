from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, email: str, username: str, password, str):
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
    if email:
        user.email = email
    if username:
        user.username = username
    if bio is not None:
        user.bio = bio
    if image is not None:
        user.image = image
    if password:
        user.password = get_password_hash(password)
    db.commit()
    db.refresh(user)
    return user
