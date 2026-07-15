# backend/app/main.py
from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import posts, comments, events, places  # ✅ 상대 import로 수정
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 허용할 프론트엔드 주소들
origins = [
    "http://localhost:5173",   # 개발용 React/Vite
    "https://localhub-1.onrender.com",  # 배포된 프론트엔드 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # 허용할 도메인 리스트
    allow_credentials=True,
    allow_methods=["*"],          # 모든 HTTP 메서드 허용
    allow_headers=["*"],          # 모든 헤더 허용
)

app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(events.router)
app.include_router(places.router)