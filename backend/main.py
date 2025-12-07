from fastapi import FastAPI
from src.routes import articles
from src.database import engine
from sqlalchemy import text
import os

app = FastAPI(title="Blog main")

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
    return {"message": "Welcome to Blog API main"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )