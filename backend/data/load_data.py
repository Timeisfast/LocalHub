# load_data.py
import json
from pathlib import Path
from .database import SessionLocal
from . import models


def load_json_to_db(file_path: str, model_class):
    """JSON 파일을 읽어 DatasetMeta + items 테이블에 저장"""
    db = SessionLocal()
    try:
        # JSON 로드
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 메타 정보 저장
        meta = models.DatasetMeta(
            region=data["region"],
            contentType=data["contentType"],
            contentTypeId=data["contentTypeId"],
            total=data["total"]
        )
        db.add(meta)
        db.commit()
        db.refresh(meta)

        # items 저장
        for item in data["items"]:
            obj = model_class.from_dict(meta.id, item)
            db.add(obj)

        db.commit()
        print(f"{file_path} → {model_class.__tablename__} 적재 완료")

    except Exception as e:
        print(f"에러 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # 프로젝트 기준의 data 디렉터리 경로를 계산
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"

    # 숙박 데이터 적재
    load_json_to_db(str(data_dir / "seoul_accommodation.json"), models.AccommodationItem)

    # 축제 데이터 적재
    load_json_to_db(str(data_dir / "seoul_festival.json"), models.FestivalItem)

    # 레포츠 데이터 적재
    load_json_to_db(str(data_dir / "seoul_leisure.json"), models.LeisureItem)

    # 여행코스 데이터 적재
    load_json_to_db(str(data_dir / "seoul_travelcourse.json"), models.TravelCourseItem)

    # 나머지 파일도 동일하게 추가 가능
    load_json_to_db(str(data_dir / "seoul_culture.json"), models.CultureItem)
    load_json_to_db(str(data_dir / "seoul_shopping.json"), models.ShoppingItem)
    load_json_to_db(str(data_dir / "seoul_tourist.json"), models.TouristItem)
