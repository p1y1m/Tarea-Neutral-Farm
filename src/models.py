from __future__ import annotations
from sqlalchemy import Column, Integer, Float
from .db import Base

class SoilRecord(Base):
    __tablename__ = "soil_records"
    id = Column(Integer, primary_key=True, index=True)
    pH = Column(Float, nullable=False)
    EC = Column(Float, nullable=False)
    total_nitrogen = Column(Float, nullable=False)
    moisture = Column(Float, nullable=False)
    organic_matter = Column(Float, nullable=True)
