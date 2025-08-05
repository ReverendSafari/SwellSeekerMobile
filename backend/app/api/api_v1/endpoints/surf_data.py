from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.db.database import get_db
from app.schemas.weather import SurfDataResponse, WindData, WaveData, TideData, TemperatureData
from app.services.cache_service import CacheService
from app.services.weather_service import WeatherService
from app.services.auth_service import AuthService
from app.services.grading_service import GradingService

router = APIRouter()

@router.get("/{beach_name}", response_model=SurfDataResponse)
async def get_surf_data(
    beach_name: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(AuthService.get_current_api_key)
):
    """Get all surf data for a beach (wind, waves, tides, temperature)"""
    beach = CacheService.get_beach_by_name(db, beach_name)
    if not beach:
        raise HTTPException(status_code=404, detail=f"Beach '{beach_name}' not found")
    
    response = SurfDataResponse(beach_name=beach_name)
    
    # Get wind data
    wind_data = await get_wind_data_internal(beach, db)
    if wind_data:
        response.wind = wind_data
    
    # Get wave data
    wave_data = await get_wave_data_internal(beach, db)
    if wave_data:
        response.waves = wave_data
    
    # Get tide data
    tide_data = await get_tide_data_internal(beach, db)
    if tide_data:
        response.tides = tide_data
    
    # Get temperature data
    temp_data = await get_temperature_data_internal(beach, db)
    if temp_data:
        response.temperature = temp_data
    
    # Calculate grade if we have both wind and wave data
    try:
        if wind_data and wave_data and wind_data.data and wave_data.data:
            grade = GradingService.calculate_grade_from_data(
                wind_data=wind_data.data,
                wave_data=wave_data.data,
                beach_orientation=beach.beach_angle
            )
            response.grade = grade
    except Exception as e:
        print(f"Error calculating grade: {e}")
        response.grade = None
    
    return response

@router.get("/{beach_name}/wind", response_model=WindData)
async def get_wind_data(
    beach_name: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(AuthService.get_current_api_key)
):
    """Get wind data for a beach"""
    beach = CacheService.get_beach_by_name(db, beach_name)
    if not beach:
        raise HTTPException(status_code=404, detail=f"Beach '{beach_name}' not found")
    
    wind_data = await get_wind_data_internal(beach, db)
    if not wind_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve wind data")
    
    return wind_data

@router.get("/{beach_name}/waves", response_model=WaveData)
async def get_wave_data(
    beach_name: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(AuthService.get_current_api_key)
):
    """Get wave data for a beach"""
    beach = CacheService.get_beach_by_name(db, beach_name)
    if not beach:
        raise HTTPException(status_code=404, detail=f"Beach '{beach_name}' not found")
    
    wave_data = await get_wave_data_internal(beach, db)
    if not wave_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve wave data")
    
    return wave_data

@router.get("/{beach_name}/tides", response_model=TideData)
async def get_tide_data(
    beach_name: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(AuthService.get_current_api_key)
):
    """Get tide data for a beach"""
    beach = CacheService.get_beach_by_name(db, beach_name)
    if not beach:
        raise HTTPException(status_code=404, detail=f"Beach '{beach_name}' not found")
    
    tide_data = await get_tide_data_internal(beach, db)
    if not tide_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve tide data")
    
    return tide_data

@router.get("/{beach_name}/temperature", response_model=TemperatureData)
async def get_temperature_data(
    beach_name: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(AuthService.get_current_api_key)
):
    """Get temperature data for a beach"""
    beach = CacheService.get_beach_by_name(db, beach_name)
    if not beach:
        raise HTTPException(status_code=404, detail=f"Beach '{beach_name}' not found")
    
    temp_data = await get_temperature_data_internal(beach, db)
    if not temp_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve temperature data")
    
    return temp_data

# Internal helper functions
async def get_wind_data_internal(beach, db: Session) -> WindData:
    """Get wind data with caching"""
    # Check cache first
    cached_data = CacheService.get_cached_data(db, beach.id, "wind_data")
    if cached_data:
        return WindData(
            beach_name=beach.beach_name,
            data=cached_data['data'],
            cached=True
        )
    
    # Fetch fresh data
    wind_data = WeatherService.get_wind_data(beach.lat, beach.long)
    if 'error' in wind_data:
        return None
    
    # Cache the data
    CacheService.store_cached_data(db, beach.id, "wind_data", wind_data)
    
    return WindData(
        beach_name=beach.beach_name,
        data=wind_data,
        cached=False
    )

async def get_wave_data_internal(beach, db: Session) -> WaveData:
    """Get wave data with caching"""
    # Check cache first
    cached_data = CacheService.get_cached_data(db, beach.id, "wave_data")
    if cached_data:
        return WaveData(
            beach_name=beach.beach_name,
            data=cached_data['data'],
            cached=True
        )
    
    # Fetch fresh data
    wave_data = WeatherService.get_wave_data(beach.lat, beach.long)
    if 'error' in wave_data:
        return None
    
    # Cache the data
    CacheService.store_cached_data(db, beach.id, "wave_data", wave_data)
    
    return WaveData(
        beach_name=beach.beach_name,
        data=wave_data,
        cached=False
    )

async def get_tide_data_internal(beach, db: Session) -> TideData:
    """Get tide data with caching"""
    # Check cache first
    cached_data = CacheService.get_cached_data(db, beach.id, "tide_data")
    if cached_data:
        return TideData(
            beach_name=beach.beach_name,
            data=cached_data['data'],
            cached=True
        )
    
    # Fetch fresh data
    tide_data = WeatherService.get_tide_data(beach.station_id)
    if 'error' in tide_data:
        return None
    
    # Cache the data
    CacheService.store_cached_data(db, beach.id, "tide_data", tide_data)
    
    return TideData(
        beach_name=beach.beach_name,
        data=tide_data,
        cached=False
    )

async def get_temperature_data_internal(beach, db: Session) -> TemperatureData:
    """Get temperature data with caching"""
    # Check cache first
    cached_data = CacheService.get_cached_data(db, beach.id, "temp_data")
    if cached_data:
        return TemperatureData(
            beach_name=beach.beach_name,
            data=cached_data['data'],
            cached=True
        )
    
    # Fetch fresh data
    temp_data = WeatherService.get_temperature_data(beach.station_id)
    if 'error' in temp_data:
        return None
    
    # Cache the data
    CacheService.store_cached_data(db, beach.id, "temp_data", temp_data)
    
    return TemperatureData(
        beach_name=beach.beach_name,
        data=temp_data,
        cached=False
    ) 