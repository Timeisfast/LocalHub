import os
import shutil
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드

# ==========================================
# [중요] 최우선 강제 복사 단계 (가장 먼저 실행됨)
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parents[1]
ORIGINAL_DB_PATH = PROJECT_ROOT / "localhub.db"

# Render 배포 서버 환경인지 확인
if os.environ.get("RENDER"):
    DB_PATH = Path("/tmp/localhub.db")
    
    # 서버 기동 시 무조건 /tmp 폴더로 복사 수행 (기존 파일 유무 상관없이 무조건 덮어쓰기 복사하여 정합성 유지)
    if ORIGINAL_DB_PATH.exists():
        try:
            shutil.copy2(ORIGINAL_DB_PATH, DB_PATH)
            print(f"📦 [Render DB] {ORIGINAL_DB_PATH} -> {DB_PATH} 복사 완료!")
        except Exception as e:
            print(f"⚠️ [Render DB] 복사 중 오류 발생: {e}")
    else:
        print("⚠️ [Render DB] 깃허브에 업로드된 localhub.db 원본 파일을 찾을 수 없습니다.")
else:
    # 로컬 개발 환경
    DB_PATH = ORIGINAL_DB_PATH

# ==========================================
# SQL Alchemy 설정 단계
# ==========================================
DATABASE_URL = os.getenv("DATABASE_URL")

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
print(f"현재 실제로 연결을 시도 중인 DB URL: {DATABASE_URL}")

# ✅ FastAPI 의존성으로 쓸 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
