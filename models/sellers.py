from sqlalchemy import Column, Integer, String
from database import Base

class Seller(Base):
    __tablename__ = "olist_sellers"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(String, unique=True, index=True)
    seller_zip_code_prefix = Column(Integer)
    seller_city = Column(String)
    seller_state = Column(String)
