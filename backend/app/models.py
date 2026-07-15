from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base
# -------------------------
# 메타 테이블
# -------------------------
class DatasetMeta(Base):
    __tablename__ = "dataset_meta"

    id = Column(Integer, primary_key=True, index=True)   # PK
    region = Column(String, index=True)                  # ex: 서울
    contentType = Column(String, index=True)             # ex: 축제공연행사
    contentTypeId = Column(Integer, index=True)          # ex: 15
    total = Column(Integer)                              # 전체 항목 수

    # 관계 설정 (1:N)
    festival_items = relationship("FestivalItem", back_populates="dataset")
    tourist_items = relationship("TouristItem", back_populates="dataset")
    culture_items = relationship("CultureItem", back_populates="dataset")
    leisure_items = relationship("LeisureItem", back_populates="dataset")
    accommodation_items = relationship("AccommodationItem", back_populates="dataset")
    shopping_items = relationship("ShoppingItem", back_populates="dataset")
    travelcourse_items = relationship("TravelCourseItem", back_populates="dataset")
    restaurant_items = relationship("RestaurantItem", back_populates="dataset")


# -------------------------
# 공통 필드 Mixin
# -------------------------
class PoiBase:
    id = Column(Integer, primary_key=True, index=True)   # PK
    dataset_id = Column(Integer, ForeignKey("dataset_meta.id"))  # FK
    contentid = Column(String, unique=True, index=True)  # 외부 데이터 고유 ID
    contenttypeid = Column(String, index=True)
    title = Column(String, index=True)
    addr1 = Column(String)
    addr2 = Column(String)
    zipcode = Column(String)
    tel = Column(String)
    mapx = Column(Float)   # DB stores Float; ingest should convert from string
    mapy = Column(Float)
    mlevel = Column(String)
    areacode = Column(String)
    sigungucode = Column(String)
    lDongRegnCd = Column(String)
    lDongSignguCd = Column(String)
    cat1 = Column(String)
    cat2 = Column(String)
    cat3 = Column(String)
    lclsSystm1 = Column(String)
    lclsSystm2 = Column(String)
    lclsSystm3 = Column(String)
    firstimage = Column(String)
    firstimage2 = Column(String)
    cpyrhtDivCd = Column(String)
    createdtime = Column(String)   # 원본은 'YYYYMMDDHHmmss' 문자열
    modifiedtime = Column(String)

    @classmethod
    def from_dict(cls, dataset_id: int, data: dict):
        """Create model instance from raw JSON dict.
        - empty strings -> None
        - mapx/mapy: try float conversion, else None
        """
        def empty_to_none(v):
            if v is None:
                return None
            if isinstance(v, str) and v.strip() == "":
                return None
            return v

        def to_float(v):
            v = empty_to_none(v)
            if v is None:
                return None
            try:
                return float(v)
            except (ValueError, TypeError):
                return None

        return cls(
            dataset_id=dataset_id,
            contentid=empty_to_none(data.get("contentid")),
            contenttypeid=empty_to_none(data.get("contenttypeid")),
            title=empty_to_none(data.get("title")),
            addr1=empty_to_none(data.get("addr1")),
            addr2=empty_to_none(data.get("addr2")),
            zipcode=empty_to_none(data.get("zipcode")),
            tel=empty_to_none(data.get("tel")),
            mapx=to_float(data.get("mapx")),
            mapy=to_float(data.get("mapy")),
            mlevel=empty_to_none(data.get("mlevel")),
            areacode=empty_to_none(data.get("areacode")),
            sigungucode=empty_to_none(data.get("sigungucode")),
            lDongRegnCd=empty_to_none(data.get("lDongRegnCd")),
            lDongSignguCd=empty_to_none(data.get("lDongSignguCd")),
            cat1=empty_to_none(data.get("cat1")),
            cat2=empty_to_none(data.get("cat2")),
            cat3=empty_to_none(data.get("cat3")),
            lclsSystm1=empty_to_none(data.get("lclsSystm1")),
            lclsSystm2=empty_to_none(data.get("lclsSystm2")),
            lclsSystm3=empty_to_none(data.get("lclsSystm3")),
            firstimage=empty_to_none(data.get("firstimage")),
            firstimage2=empty_to_none(data.get("firstimage2")),
            cpyrhtDivCd=empty_to_none(data.get("cpyrhtDivCd")),
            createdtime=empty_to_none(data.get("createdtime")),
            modifiedtime=empty_to_none(data.get("modifiedtime")),
        )


# -------------------------
# 카테고리별 테이블
# -------------------------
class FestivalItem(PoiBase, Base):
    __tablename__ = "festival_items"
    dataset = relationship("DatasetMeta", back_populates="festival_items")
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    
class TouristItem(PoiBase, Base):
    __tablename__ = "tourist_items"
    dataset = relationship("DatasetMeta", back_populates="tourist_items")

class CultureItem(PoiBase, Base):
    __tablename__ = "culture_items"
    dataset = relationship("DatasetMeta", back_populates="culture_items")

class LeisureItem(PoiBase, Base):
    __tablename__ = "leisure_items"
    dataset = relationship("DatasetMeta", back_populates="leisure_items")

class AccommodationItem(PoiBase, Base):
    __tablename__ = "accommodation_items"
    dataset = relationship("DatasetMeta", back_populates="accommodation_items")

class ShoppingItem(PoiBase, Base):
    __tablename__ = "shopping_items"
    dataset = relationship("DatasetMeta", back_populates="shopping_items")

class TravelCourseItem(PoiBase, Base):
    __tablename__ = "travelcourse_items"
    dataset = relationship("DatasetMeta", back_populates="travelcourse_items")

class RestaurantItem(PoiBase, Base):
    __tablename__ = "restaurant_items"
    dataset = relationship("DatasetMeta", back_populates="restaurant_items")