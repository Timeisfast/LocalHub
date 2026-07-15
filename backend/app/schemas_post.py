from pydantic import BaseModel
from datetime import datetime

# 공통 필드
class PostBase(BaseModel):
    title: str
    content: str
    author: str = "익명"

# 글 작성 시 요청 스키마
class PostCreate(PostBase):
    password: str

# 글 조회/응답 스키마
class PostResponse(PostBase):
    id: int
    created_at: datetime | None 
    views: int

    class Config:
        from_attributes  = True   # SQLAlchemy 모델을 Pydantic으로 변환 가능하게 설정
