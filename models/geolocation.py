from sqlalchemy import Column, Integer, Float, String
from database import Base

class Geolocation(Base):
    __tablename__ = "olist_geolocation"
    id = Column(Integer, primary_key=True, index=True)
    geolocation_zip_code_prefix = Column(Integer, index=True)
    geolocation_lat = Column(Float)
    geolocation_lng = Column(Float)
    geolocation_city = Column(String)
    geolocation_state = Column(String)
