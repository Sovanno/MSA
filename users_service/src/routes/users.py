from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from users_service.src.auth import get_db
from users_service.src.controllers.user_controller import create_user, authenticate_user, update_user
from users_service.src.auth import create_access_token, get_current_user
from users_service.src import schemas

router = APIRouter(prefix="/api")


@router.post("/users", tags=["users"])
async def register_user(payload: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = create_user(db, payload.email, payload.username, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    token = create_access_token({"user_id": user.id, "username": user.username})
    return schemas.UserResponse(email=user.email, username=user.username, bio=user.bio, image=user.image, token=token)


@router.post("/users/login", tags=["users"])
async def login_user(payload: schemas.LoginRequest, db: AsyncSession = Depends(get_db)):
    email = payload.email
    password = payload.password
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Неправильный email или пароль")
    token = create_access_token({"user_id": user.id, "username": user.username})
    return schemas.UserResponse(email=user.email, username=user.username, bio=user.bio, image=user.image, token=token)


@router.get("/user", tags=["users"])
def get_current_user_route(current_user = Depends(get_current_user)):
    return schemas.UserResponse(email=current_user.email, username=current_user.username, bio=current_user.bio, image=current_user.image)


@router.put("/user", tags=["users"])
async def update_current_user(payload: schemas.UserUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        user = update_user(db, current_user, email=payload.email, username=payload.username, bio=payload.bio, image=payload.image, password=payload.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return schemas.UserResponse(email=user.email, username=user.username, bio=user.bio, image=user.image)
