from fastapi import FastAPI
from src.routes import users
from src.database import engine
from sqlalchemy import text
import os

app = FastAPI(title="Blog users")

app.include_router(users.router)


@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}


@app.get("/")
def read_root():
    return {"message": "Welcome to Blog API users"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "user:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )