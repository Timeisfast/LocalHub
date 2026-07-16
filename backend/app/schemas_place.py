from pydantic import BaseModel

# 공통 필드 (관광지/쇼핑 모두 사용)
class PlaceBase(BaseModel):
    id: int
    contentid: str | None = None
    contenttypeid: str | None = None
    title: str
    addr1: str | None = None
    addr2: str | None = None
    zipcode: str | None = None
    tel: str | None = None
    mapx: float | None = None   # 네이버 지도 SDK 좌표
    mapy: float | None = None
    firstimage: str | None = None
    firstimage2: str | None = None

    class Config:
        from_attributes = True

# 상세 조회용 (공통 필드 + 추가 정보)
class PlaceDetail(PlaceBase):
    mlevel: str | None = None
    areacode: str | None = None
    sigungucode: str | None = None
    cat1: str | None = None
    cat2: str | None = None
    cat3: str | None = None
    createdtime: str | None = None
    modifiedtime: str | None = None
    description: str | None = None
