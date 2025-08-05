from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BeachBase(BaseModel):
    beach_name: str
    town: str
    state: str
    lat: float
    long: float
    beach_angle: float
    station_id: str

class BeachCreate(BeachBase):
    pass

class Beach(BeachBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class BeachList(BaseModel):
    beaches: list[Beach] 