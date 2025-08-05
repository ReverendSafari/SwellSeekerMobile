from sqlalchemy.orm import Session
from app.models.api_key import APIKey
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.database import get_db
import hashlib
from datetime import datetime

security = HTTPBearer()

class AuthService:
    """Service for API key authentication"""
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash an API key for storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    @staticmethod
    def validate_api_key(db: Session, api_key: str) -> bool:
        """Validate an API key"""
        key_hash = AuthService.hash_api_key(api_key)
        
        api_key_record = db.query(APIKey).filter(
            APIKey.key_hash == key_hash,
            APIKey.is_active == True
        ).first()
        
        if api_key_record:
            # Update last used timestamp
            api_key_record.last_used = datetime.utcnow()
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def get_current_api_key(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ) -> str:
        """Dependency for getting and validating the current API key"""
        if not credentials:
            raise HTTPException(status_code=401, detail="API key required")
        
        if not AuthService.validate_api_key(db, credentials.credentials):
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        return credentials.credentials 