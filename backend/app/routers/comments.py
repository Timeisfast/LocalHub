from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models_comment, schemas_comment

router = APIRouter(prefix="/comments", tags=["comments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 댓글 작성
@router.post("/", response_model=schemas_comment.CommentResponse)
def create_comment(comment: schemas_comment.CommentCreate, post_id: int, db: Session = Depends(get_db)):
    new_comment = models_comment.Comment(post_id=post_id, content=comment.content, author=comment.author)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# 특정 게시글 댓글 조회
@router.get("/{post_id}", response_model=list[schemas_comment.CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return db.query(models_comment.Comment).filter(models_comment.Comment.post_id == post_id).all()

# 댓글 삭제
@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(models_comment.Comment).filter(models_comment.Comment.id == comment_id).first()
    if not db_comment:
        return {"error": "댓글을 찾을 수 없습니다."}
    db.delete(db_comment)
    db.commit()
    return {"message": "댓글이 삭제되었습니다."}
