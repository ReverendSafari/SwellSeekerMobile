from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.beach import Beach, BeachList
from app.services.cache_service import CacheService
from app.services.auth_service import AuthService

router = APIRouter()

@router.get("/", response_model=BeachList)
async def get_beaches(
    db: Session = Depends(get_db),
    api_key: str = Depends(AuthService.get_current_api_key)
):
    """Get all beaches"""
    beaches = CacheService.get_all_beaches(db)
    return BeachList(beaches=beaches)

@router.get("/{beach_name}", response_model=Beach)
async def get_beach(
    beach_name: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(AuthService.get_current_api_key)
):
    """Get a specific beach by name"""
    beach = CacheService.get_beach_by_name(db, beach_name)
    if not beach:
        raise HTTPException(status_code=404, detail=f"Beach '{beach_name}' not found")
    return beach 