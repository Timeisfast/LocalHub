from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas_place

router = APIRouter(prefix="/places", tags=["places"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 카테고리별 장소 목록 조회 (지도 마커용)
@router.get("/", response_model=list[schemas_place.PlaceBase])
def get_places(category: str = Query(..., regex="^(tourist|shopping)$"), db: Session = Depends(get_db)):
    if category == "tourist":
        return db.query(models.TouristItem).all()
    elif category == "shopping":
        return db.query(models.ShoppingItem).all()

# 장소 상세 조회 (핀 클릭 시)
@router.get("/{place_id}", response_model=schemas_place.PlaceDetail)
def get_place_detail(place_id: int, category: str = Query(..., regex="^(tourist|shopping)$"), db: Session = Depends(get_db)):
    if category == "tourist":
        return db.query(models.TouristItem).filter(models.TouristItem.id == place_id).first()
    elif category == "shopping":
        return db.query(models.ShoppingItem).filter(models.ShoppingItem.id == place_id).first()

# 장소 관련 커뮤니티 게시글 조회
@router.get("/{place_id}/posts")
def get_place_posts(place_id: int, db: Session = Depends(get_db)):
    return db.query(models.Post).filter(models.Post.place_id == place_id).all()

# 장소 관련 커뮤니티 게시글 작성
@router.post("/{place_id}/posts")
def create_place_post(place_id: int, post: dict, db: Session = Depends(get_db)):
    new_post = models.Post(place_id=place_id, **post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
