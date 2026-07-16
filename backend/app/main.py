
# backend/app/main.py
from fastapi import FastAPI
from pathlib import Path
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import models
from .routers import posts, comments, events, places, chat    # ✅ 상대 import로 수정

Base.metadata.create_all(bind=engine)


# LocalHub/.env 로드
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="LocalHub API",
    description="서울 지역 관광·축제·음식점·커뮤니티 API",
    version="1.0.0",
)


# 허용할 프론트엔드 주소들
origins = [
    "http://localhost:5173",   # 개발용 React/Vite
    "https://localhub3.netlify.app",  # 배포된 프론트엔드 주소
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
app.include_router(chat.router)


@app.get("/health", include_in_schema=False)
def health_check():
    return {
        "status": "ok",
        "service": "LocalHub API",
    }
