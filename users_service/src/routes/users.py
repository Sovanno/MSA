from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import get_db
from src.controllers.user_controller import create_user, authenticate_user, update_user, \
    update_subscription_key, subscribe_to_author, unsubscribe_from_author, get_subscribers_with_keys, \
    get_user_subscriptions, is_subscribed
from src.auth import create_access_token, get_current_user
from src import schemas

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

@router.put("/users/me/subscription-key", tags=["subscribe"])
async def update_subscription_key_route(
    payload: schemas.SubscriptionKeyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        user = await update_subscription_key(db, current_user, payload.subscription_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return schemas.UserResponse(
        email=user.email,
        username=user.username,
        bio=user.bio,
        image=user.image,
        subscription_key=user.subscription_key
    )

@router.post("/users/subscribe", tags=["subscribe"])
async def subscribe_to_author_route(
    payload: schemas.SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        await subscribe_to_author(db, current_user.id, payload.target_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Подписка прошла успешна"}

@router.post("/users/unsubscribe", tags=["subscribe"])
async def subscribe_to_author_route(
    payload: schemas.SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        await unsubscribe_from_author(db, current_user.id, payload.target_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Отписка прошла успешна"}

@router.get("/users/{author_id}/subscribers", tags=["subscribe"])
async def get_subscribers_route(
    author_id: int,
    db: AsyncSession = Depends(get_db)
):
    subscribers = await get_subscribers_with_keys(db, author_id)
    return {"subscribers": subscribers}

@router.get("/users/me/subscriptions", tags=["subscribe"])
async def get_subscribers_route(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    subscribers = await get_user_subscriptions(db, current_user.id)
    return {"subscriptions": subscribers}

@router.get("/users/{author_id}/is-subscriptions", tags=["subscribe"])
async def get_subscribers_route(
    payload: schemas.SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    subscribers = await is_subscribed(db, current_user.id, payload.target_user_id)
    return {"Подписан": subscribers}
