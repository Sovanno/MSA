from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from config import settings

USERS_JWT_SECRET = settings.jwt_secret
ALGORITHM = "HS256"

security = HTTPBearer()


class TokenUser:
    def __init__(self, id: int, username: Optional[str] = None, email: Optional[str] = None):
        self.id = int(id)
        self.username = username
        self.email = email


def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"}
    )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenUser:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, USERS_JWT_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")
        email = payload.get("email")
        if user_id is None:
            raise credentials_exception()
    except JWTError:
        raise credentials_exception()

    return TokenUser(id=user_id, username=username, email=email)
