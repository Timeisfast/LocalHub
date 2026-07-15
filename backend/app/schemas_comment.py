from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    content: str
    author: str = "익명"

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True
