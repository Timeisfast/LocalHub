from pydantic import BaseModel

class FestivalResponse(BaseModel):
    id: int
    contentid: str | None = None
    contenttypeid: str | None = None
    title: str
    addr1: str | None = None
    addr2: str | None = None
    zipcode: str | None = None
    tel: str | None = None
    mapx: float | None = None
    mapy: float | None = None
    mlevel: str | None = None
    areacode: str | None = None
    sigungucode: str | None = None
    lDongRegnCd: str | None = None
    lDongSignguCd: str | None = None
    cat1: str | None = None
    cat2: str | None = None
    cat3: str | None = None
    lclsSystm1: str | None = None
    lclsSystm2: str | None = None
    lclsSystm3: str | None = None
    firstimage: str | None = None
    firstimage2: str | None = None
    cpyrhtDivCd: str | None = None
    createdtime: str | None = None
    modifiedtime: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True
        orm_mode = True
