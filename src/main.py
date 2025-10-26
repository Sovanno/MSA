from fastapi import FastAPI
from src.routes import users, articles
from src.database import base
from src.database import engine

app = FastAPI(title="Blog")

base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(articles.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
