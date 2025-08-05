import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json

class WeatherService:
    """Service for fetching weather data from external APIs"""
    
    @staticmethod
    def get_wind_data(lat: float, long: float) -> Dict[str, Any]:
        """Fetch wind data from Open-Meteo API"""
        wind_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=wind_speed_10m,wind_direction_10m&temperature_unit=fahrenheit&wind_speed_unit=kn&timezone=America%2FNew_York&temporal_resolution=hourly_3&cell_selection=sea"
        
        try:
            response = requests.get(wind_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_error:
            print(f"HTTP Error occurred: {http_error}")
            return {'error': f"HTTP error occurred: {http_error}"}
        except Exception as err:
            print(f"General Error occurred: {err}")
            return {'error': f"General error occurred: {err}"}
    
    @staticmethod
    def get_wave_data(lat: float, long: float) -> Dict[str, Any]:
        """Fetch wave data from Open-Meteo Marine API"""
        waves_url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={long}&hourly=wave_height,wave_direction,wave_period&length_unit=imperial&timezone=America%2FNew_York&temporal_resolution=hourly_3&models=ncep_gfswave025"
        
        try:
            response = requests.get(waves_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_error:
            print(f"HTTP Error occurred: {http_error}")
            return {'error': f"HTTP error occurred: {http_error}"}
        except Exception as err:
            print(f"General Error occurred: {err}")
            return {'error': f"General error occurred: {err}"}
    
    @staticmethod
    def get_tide_data(station_id: str) -> Dict[str, Any]:
        """Fetch tide data from NOAA API"""
        tides_url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=today&station={station_id}&product=predictions&datum=STND&time_zone=lst&interval=hilo&units=english&format=json"
        
        try:
            response = requests.get(tides_url)
            response.raise_for_status()
            tide_data = response.json()
            tide_predictions = tide_data.get('predictions', [])
            
            formatted_data = []
            for tide in tide_predictions:
                formatted_data.append({
                    'time': tide['t'],
                    'height': tide['v'],
                    'type': 'high' if tide['type'] == 'H' else 'low'
                })
            
            return formatted_data
        except requests.exceptions.HTTPError as http_error:
            print(f"HTTP Error occurred: {http_error}")
            return {'error': f"HTTP error occurred: {http_error}"}
        except Exception as err:
            print(f"General Error occurred: {err}")
            return {'error': f"General error occurred: {err}"}
    
    @staticmethod
    def get_temperature_data(station_id: str) -> Dict[str, Any]:
        """Fetch temperature data from NOAA API"""
        air_temp_url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station={station_id}&product=air_temperature&datum=STND&time_zone=lst&units=english&format=json"
        water_temp_url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?date=latest&station={station_id}&product=water_temperature&datum=STND&time_zone=lst&units=english&format=json"
        
        try:
            # Get water temperature
            water_temp_response = requests.get(water_temp_url)
            water_temp_response.raise_for_status()
            water_temp_data = water_temp_response.json()
            water_temp = water_temp_data['data'][0]['v']
            
            # Get air temperature
            air_temp_response = requests.get(air_temp_url)
            air_temp_response.raise_for_status()
            air_temp_data = air_temp_response.json()
            air_temp = air_temp_data['data'][0]['v']
            
            return {
                "station_id": station_id,
                "water_temp": water_temp,
                "air_temp": air_temp
            }
        except requests.exceptions.HTTPError as http_error:
            print(f"HTTP Error occurred: {http_error}")
            return {'error': f"HTTP error occurred: {http_error}"}
        except Exception as err:
            print(f"General Error occurred: {err}")
            return {'error': f"General error occurred: {err}"} 