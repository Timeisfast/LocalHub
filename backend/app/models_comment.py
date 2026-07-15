from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from . import models_post

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))   # 게시글 FK
    content = Column(String, nullable=False)
    author = Column(String, default="익명")
    created_at = Column(DateTime, default=datetime.now)

    post = relationship("Post", back_populates="comments")
