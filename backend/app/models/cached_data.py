from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class CachedData(Base):
    __tablename__ = "cached_data"
    
    id = Column(Integer, primary_key=True, index=True)
    beach_id = Column(Integer, ForeignKey("beaches.id"), nullable=False)
    data_type = Column(String, nullable=False)  # 'wind_data', 'wave_data', 'tide_data', 'temp_data'
    data = Column(JSON, nullable=False)  # Store the actual API response data
    expires_at = Column(DateTime(timezone=True), nullable=False)  # TTL timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    beach = relationship("Beach", back_populates="cached_data")
    
    __table_args__ = (
        # Ensure one record per beach per data type
        # This allows us to easily replace old data with new data
    ) 