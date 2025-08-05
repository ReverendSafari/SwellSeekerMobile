from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime

class WeatherDataBase(BaseModel):
    beach_name: str
    data_type: str
    data: Any
    cached: bool = False

class WindData(WeatherDataBase):
    data_type: str = "wind_data"

class WaveData(WeatherDataBase):
    data_type: str = "wave_data"

class TideData(WeatherDataBase):
    data_type: str = "tide_data"

class TemperatureData(WeatherDataBase):
    data_type: str = "temp_data"

class SurfDataResponse(BaseModel):
    beach_name: str
    wind: Optional[WindData] = None
    waves: Optional[WaveData] = None
    tides: Optional[TideData] = None
    temperature: Optional[TemperatureData] = None
    grade: Optional[str] = None  # 'red', 'yellow', or 'green'
    cached: bool = False

class TidePrediction(BaseModel):
    time: str
    height: str
    type: str  # 'high' or 'low'

class TemperatureResponse(BaseModel):
    station_id: str
    water_temp: str
    air_temp: str 