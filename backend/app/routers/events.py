from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas_event

router = APIRouter(prefix="/events", tags=["events"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 축제 목록 조회
@router.get("/", response_model=list[schemas_event.FestivalResponse])
def get_festivals(db: Session = Depends(get_db)):
    return db.query(models.FestivalItem).all()

# 특정 축제 조회
@router.get("/{event_id}", response_model=schemas_event.FestivalResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    return db.query(models.FestivalItem).filter(models.FestivalItem.id == event_id).first()
