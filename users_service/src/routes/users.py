from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.controllers.user_controller import create_user, authenticate_user, update_user
from src.auth import create_access_token, get_current_user
from src import schemas
from src import models
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

router = APIRouter(prefix="/api")


@router.post("/users", tags=["users"])
async def register_user(payload: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await create_user(db, payload.email, payload.username, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    token = create_access_token({"user_id": user.id, "username": user.username})
    return schemas.UserResponse(email=user.email, username=user.username, bio=user.bio, image=user.image, token=token)

@router.post("/users/login", tags=["users"])
async def login_user(payload: schemas.LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="Неправильный email или пароль")
    token = create_access_token({"user_id": user.id, "username": user.username})
    return schemas.UserResponse(email=user.email, username=user.username, bio=user.bio, image=user.image, token=token)

@router.get("/user", tags=["users"])
async def get_current_user_route(current_user=Depends(get_current_user)):
    return schemas.UserResponse(email=current_user.email, username=current_user.username, bio=current_user.bio, image=current_user.image)

@router.put("/user", tags=["users"])
async def update_current_user(payload: schemas.UserUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        user = await update_user(db, current_user, email=payload.email, username=payload.username, bio=payload.bio, image=payload.image, password=payload.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return schemas.UserResponse(email=user.email, username=user.username, bio=user.bio, image=user.image)

class SubscriptionKeyIn(BaseModel):
    subscription_key: str

@router.put("/users/me/subscription-key", tags=["subscribe"])
async def put_subscription_key(payload: SubscriptionKeyIn, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    current_user.subscription_key = payload.subscription_key
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "subscription_key_set": bool(current_user.subscription_key)
    }

class SubscribeIn(BaseModel):
    target_user_id: int

@router.post("/users/subscribe", status_code=204, tags=["subscribe"])
async def subscribe(payload: SubscribeIn, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.id == payload.target_user_id:
        raise HTTPException(status_code=400, detail="Cannot subscribe to yourself")

    sub = models.subscriptions.Subscriber(subscriber_id=current_user.id, author_id=payload.target_user_id)
    db.add(sub)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
    return
