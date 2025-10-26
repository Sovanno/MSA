from fastapi import FastAPI
from src.routes import users, articles
from src.database import base
from src.database import engine
from sqlalchemy import text
import os

app = FastAPI(title="Blog")

base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(articles.router)


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
    return {"message": "Welcome to Blog API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )