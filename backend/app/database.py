from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


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