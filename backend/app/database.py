import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

DATABASE_URL = os.getenv("DATABASE_URL")

# 1. database.py 파일이 있는 위치를 기준으로 프로젝트 루트 디렉토리를 절대 경로로 계산합니다.
# LocalHub/backend/app/database.py 이므로 .parent.parent.parent가 실제 프로젝트 루트입니다.
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[1]

# 2. 업로드한 localhub.db 파일의 실제 절대 경로를 구합니다.
DB_PATH = PROJECT_ROOT / "localhub.db"

# 3. 데이터베이스 URL이 없을 때 파일이 존재하는 절대 경로를 주입합니다.
if not DATABASE_URL:
    # 절대 경로인지 다시 한번 체크하여 sqlite:/// 형식을 완성합니다.
    DATABASE_URL = f"sqlite:///{DB_PATH.resolve().as_posix()}"

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

# DB 경로 확인용 출력
print(f"현재 연결된 DB URL: {DATABASE_URL}")

# ✅ FastAPI 의존성으로 쓸 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
