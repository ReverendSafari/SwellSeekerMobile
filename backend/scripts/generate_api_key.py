import secrets
import hashlib
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.api_key import APIKey

def generate_api_key(name: str = "test-key") -> str:
    """Generate a new API key and store it in the database"""
    # Generate a random API key
    api_key = secrets.token_urlsafe(32)
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    # Store in database
    db = SessionLocal()
    try:
        api_key_record = APIKey(
            key_hash=key_hash,
            name=name
        )
        db.add(api_key_record)
        db.commit()
        
        print(f"Generated API key: {api_key}")
        print(f"Name: {name}")
        print("Store this key securely - it won't be shown again!")
        
        return api_key
    except Exception as e:
        print(f"Error generating API key: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    generate_api_key() 