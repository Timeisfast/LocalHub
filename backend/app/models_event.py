from sqlalchemy import Column, String, Integer, Text
from .database import Base

# class FestivalItem(Base):
#     __tablename__ = "festival_items"
#     __table_args__ = {'extend_existing': True}

#     id = Column(Integer, primary_key=True, index=True)
#     contentid = Column(String)
#     contenttypeid = Column(String)
#     title = Column(String)
#     addr1 = Column(String)
#     addr2 = Column(String)
#     zipcode = Column(String)
#     tel = Column(String)
#     mapx = Column(String)
#     mapy = Column(String)
#     mlevel = Column(String)
#     areacode = Column(String)
#     sigungucode = Column(String)
#     lDongRegnCd = Column(String)
#     lDongSignguCd = Column(String)
#     cat1 = Column(String)
#     cat2 = Column(String)
#     cat3 = Column(String)
#     lclsSystm1 = Column(String)
#     lclsSystm2 = Column(String)
#     lclsSystm3 = Column(String)
#     firstimage = Column(String)
#     firstimage2 = Column(String)
#     cpyrhtDivCd = Column(String)
#     createdtime = Column(String)
#     modifiedtime = Column(String)

#     start_date = Column(String, nullable=True)
#     end_date = Column(String, nullable=True)
#     description = Column(Text, nullable=True)