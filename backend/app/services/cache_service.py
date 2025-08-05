from sqlalchemy.orm import Session
from app.models.cached_data import CachedData
from app.models.beach import Beach
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import json

class CacheService:
    """Service for handling data caching with TTL"""
    
    CACHE_DURATION_HOURS = 12  # 12 hours cache duration
    
    @staticmethod
    def get_cached_data(db: Session, beach_id: int, data_type: str) -> Optional[Dict[str, Any]]:
        """Get cached data if it exists and is not expired"""
        cached_record = db.query(CachedData).filter(
            CachedData.beach_id == beach_id,
            CachedData.data_type == data_type
        ).first()
        
        # Use timezone-aware datetime for comparison
        current_time = datetime.now(timezone.utc)
        
        if cached_record:
            expires_at = cached_record.expires_at
            # Patch: If expires_at is naive, make it UTC-aware
            if expires_at.tzinfo is None or expires_at.tzinfo.utcoffset(expires_at) is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if expires_at > current_time:
                return {
                    'data': cached_record.data,
                    'cached': True,
                    'expires_at': expires_at
                }
        
        return None
    
    @staticmethod
    def store_cached_data(db: Session, beach_id: int, data_type: str, data: Dict[str, Any]) -> None:
        """Store new data in cache, replacing any existing data"""
        # Delete existing cached data for this beach and data type
        db.query(CachedData).filter(
            CachedData.beach_id == beach_id,
            CachedData.data_type == data_type
        ).delete()
        
        # Calculate expiration time with timezone-aware datetime
        expires_at = datetime.now(timezone.utc) + timedelta(hours=CacheService.CACHE_DURATION_HOURS)
        
        # Create new cached data record
        cached_data = CachedData(
            beach_id=beach_id,
            data_type=data_type,
            data=data,
            expires_at=expires_at
        )
        
        db.add(cached_data)
        db.commit()
    
    @staticmethod
    def get_beach_by_name(db: Session, beach_name: str) -> Optional[Beach]:
        """Get beach by name"""
        return db.query(Beach).filter(Beach.beach_name == beach_name).first()
    
    @staticmethod
    def get_all_beaches(db: Session) -> list[Beach]:
        """Get all beaches"""
        return db.query(Beach).all() 