import os
import shutil
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

DATABASE_URL = os.getenv("DATABASE_URL")

# 1. 원본 파일 위치 찾기 (깃허브로 업로드된 프로젝트 루트 내 localhub.db)
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[1]
ORIGINAL_DB_PATH = PROJECT_ROOT / "localhub.db"

# 2. Render 서버 환경인지 확인
if os.environ.get("RENDER"):
    # 쓰기 권한이 보장되는 /tmp 디렉토리 경로 지정
    RENDER_DB_PATH = Path("/tmp/localhub.db")
    
    # 서버 실행 시 최초 1회만 원본 DB 파일을 /tmp로 복사 (이미 있으면 덮어쓰지 않고 재사용)
    if ORIGINAL_DB_PATH.exists() and not RENDER_DB_PATH.exists():
        try:
            shutil.copy2(ORIGINAL_DB_PATH, RENDER_DB_PATH)
            print("Successfully copied database file to /tmp")
        except Exception as e:
            print(f"Failed to copy database: {e}")
            
    DB_PATH = RENDER_DB_PATH
else:
    # 로컬 개발 환경에서는 기존 경로 그대로 사용
    DB_PATH = ORIGINAL_DB_PATH

# 3. 데이터베이스 URL 설정
if not DATABASE_URL:
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
