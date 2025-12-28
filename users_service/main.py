# users_service/src/main.py
from fastapi import FastAPI
from src.routes import users
from src.database import engine, base
import os
import asyncio

app = FastAPI(title="Blog users", openapi_url="/users/openapi.json", docs_url="/users/docs")

app.include_router(users.router)


async def create_tables():
    """Создание таблиц при запуске приложения"""
    try:
        async with engine.begin() as conn:
            # Создаем все таблицы, определенные в моделях
            await conn.run_sync(base.metadata.create_all)
            print("✅ Database tables created/verified")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise


@app.on_event("startup")
async def startup_event():
    """Событие при запуске приложения"""
    print("🚀 Starting users service...")
    await create_tables()


@app.get("/health")
async def health():
    """Health check endpoint"""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "service": "users"}
    except Exception as e:
        return {"status": "error", "details": str(e), "service": "users"}


@app.get("/")
def read_root():
    return {"message": "Welcome to Blog API users service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )