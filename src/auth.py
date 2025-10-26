from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src import models
from src.database import sessinlocal
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_db() -> Generator[Session, None, None]:
    db = sessinlocal()
    try:
        yield db
    finally:
        db.close()


def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"}
    )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Token decoded successfully: {payload}")
        user_id = int(payload.get("user_id"))
        print(f"🔍 User ID from token: {user_id} (type: {type(user_id)})")
        if user_id is None:
            print(123456)
            raise credentials_exception()
    except JWTError as e:
        print(f"Error type: {type(e).__name__}")
        raise credentials_exception()
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    if user is None:
        print("-----------------")
        raise credentials_exception()
    return user

#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3NjE0OTA4NDd9.44JYq_2KCQI3hqvZqJwOBRwBHloF1OF250DFDy_JYJA
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3NjE0OTA5MjB9.WcVnMWPxTRpggpjbBpuPB8RoSroUKdTLQEPU_PTovGE