# app/routers/posts.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal        # ✅ 상대 import
from .. import models_post, schemas_post   # ✅ 상대 import

router = APIRouter(prefix="/posts", tags=["posts"])

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 게시글 목록 조회
@router.get("/", response_model=list[schemas_post.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models_post.Post).order_by(models_post.Post.id.desc()).all()
    return posts


# 게시글 작성 API
@router.post("/", response_model=schemas_post.PostResponse)
def create_post(post: schemas_post.PostCreate, db: Session = Depends(get_db)):
    new_post = models_post.Post(
        # 여기에 데이터를 수정해주는 것 같다 
        title=post.title,
        content=post.content,
        author=post.author,
        password=post.password
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# 게시글 상세 조회
@router.get("/{post_id}", response_model=schemas_post.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models_post.Post).filter(models_post.Post.id == post_id).first()
    if post:
        # 여기에도 이제 데이터 늘려서 봐주는 것 같다 
        post.views += 1  # 조회수 증가
        db.commit()
        db.refresh(post)
    return post

# 게시글 수정 API
@router.put("/{post_id}")
def update_post(post_id: int, post: schemas_post.PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(models_post.Post).filter(models_post.Post.id == post_id).first()
    if not db_post:
        return {"error": "게시글을 찾을 수 없습니다."}
    if db_post.password != post.password:
        return {"error": "비밀번호가 일치하지 않습니다."}

    db_post.title = post.title
    db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return {"message": "게시글이 수정되었습니다."}


# 게시글 삭제 API
@router.delete("/{post_id}")
def delete_post(post_id: int, password: str, db: Session = Depends(get_db)):
    db_post = db.query(models_post.Post).filter(models_post.Post.id == post_id).first()
    if not db_post:
        return {"error": "게시글을 찾을 수 없습니다."}
    if db_post.password != password:
        return {"error": "비밀번호가 일치하지 않습니다."}

    db.delete(db_post)
    db.commit()
    return {"message": "게시글이 삭제되었습니다."}



# 게시글 검색 API
@router.get("/search", response_model=list[schemas_post.PostResponse])
def search_posts(keyword: str, db: Session = Depends(get_db)):
    posts = db.query(models_post.Post).filter(
        models_post.Post.title.contains(keyword) |
        models_post.Post.content.contains(keyword) |
        models_post.Post.author.contains(keyword)
    ).order_by(models_post.Post.id.desc()).all()
    return posts


# 게시글 목록 조회 (페이징)
@router.get("/page", response_model=list[schemas_post.PostResponse])
def get_posts_page(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    skip = (page - 1) * size
    posts = (
        db.query(models_post.Post)
        .order_by(models_post.Post.id.desc())
        .offset(skip)
        .limit(size)
        .all()
    )
    return posts


