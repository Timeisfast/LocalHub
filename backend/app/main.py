# backend/app/main.py
from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import posts, comments, events, places  # ✅ 상대 import로 수정

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(events.router)
app.include_router(places.router)