import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

DATABASE_URL = os.getenv("DATABASE_URL")


# 현재 파일 위치:
# LocalHub/backend/app/database.py
#
# parent       → LocalHub/backend/app
# parents[1]   → LocalHub/backend
# parents[2]   → LocalHub
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 실제 DB 위치:
# LocalHub/localhub.db
DB_PATH = PROJECT_ROOT / "localhub.db"


if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# DB 경로 확인용
print(f"현재 연결된 DB: {DB_PATH}")

# ✅ FastAPI 의존성으로 쓸 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()