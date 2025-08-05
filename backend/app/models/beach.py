from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class Beach(Base):
    __tablename__ = "beaches"
    
    id = Column(Integer, primary_key=True, index=True)
    beach_name = Column(String, unique=True, index=True, nullable=False)
    town = Column(String, nullable=False)
    state = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    beach_angle = Column(Float, nullable=False)
    station_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    cached_data = relationship("CachedData", back_populates="beach") 