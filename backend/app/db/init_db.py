from sqlalchemy.orm import Session
from app.db.database import engine, Base
from app.models import beach, cached_data, api_key
import json
import os

def init_db():
    """Initialize the database with tables and initial data"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Import initial beach data if beaches.json exists
    beaches_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "beaches.json")
    if os.path.exists(beaches_file):
        import_beaches_from_json(beaches_file)

def import_beaches_from_json(json_file_path: str):
    """Import beach data from the old beaches.json file"""
    from app.models.beach import Beach
    from app.db.database import SessionLocal
    
    db = SessionLocal()
    try:
        with open(json_file_path, 'r') as f:
            beaches_data = json.load(f)
        
        for beach_item in beaches_data:
            item = beach_item["PutRequest"]["Item"]
            
            # Check if beach already exists
            existing_beach = db.query(Beach).filter(Beach.beach_name == item["beach_name"]["S"]).first()
            if existing_beach:
                continue
            
            # Create new beach record
            beach = Beach(
                beach_name=item["beach_name"]["S"],
                town=item["town"]["S"],
                state=item["state"]["S"],
                lat=float(item["lat"]["N"]),
                long=float(item["long"]["N"]),
                beach_angle=float(item["beach_angle"]["N"]),
                station_id=item["station_id"]["N"]
            )
            db.add(beach)
        
        db.commit()
        print(f"Imported {len(beaches_data)} beaches from JSON file")
        
    except Exception as e:
        print(f"Error importing beaches: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 