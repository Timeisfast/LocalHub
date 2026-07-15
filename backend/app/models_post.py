from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship   # ✅ 여기서 import
from datetime import datetime
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)   # PK
    title = Column(String, nullable=False)               # 글 제목
    content = Column(String, nullable=False)             # 글 내용
    author = Column(String, default="익명")              # 작성자 (기본값 익명)
    password = Column(String, nullable=False)            # 수정/삭제용 비밀번호
    created_at = Column(DateTime, default=datetime.now)  # 작성일시
    views = Column(Integer, default=0)                   # 조회수

    comments = relationship("Comment", back_populates="post", cascade="all, delete")
