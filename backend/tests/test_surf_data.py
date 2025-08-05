import pytest
from unittest.mock import patch, MagicMock
from fastapi import status
from datetime import datetime, timezone, timedelta

from app.models.beach import Beach
from app.models.api_key import APIKey
from app.models.cached_data import CachedData
from app.services.auth_service import AuthService

class TestSurfDataEndpoints:
    """Test cases for surf data endpoints"""
    
    def test_get_surf_data_without_auth(self, client):
        """Test getting surf data without authentication should fail"""
        response = client.get("/api/v1/surf-data/Test%20Beach")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_surf_data_with_invalid_auth(self, client):
        """Test getting surf data with invalid API key should fail"""
        response = client.get(
            "/api/v1/surf-data/Test%20Beach",
            headers={"Authorization": "Bearer invalid_key"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_surf_data_beach_not_found(self, client, db_session, api_key):
        """Test getting surf data for non-existent beach"""
        # Create test API key (hash the key for storage)
        key_hash = AuthService.hash_api_key(api_key)
        test_key = APIKey(key_hash=key_hash, name="test_key", is_active=True)
        db_session.add(test_key)
        db_session.commit()
        
        response = client.get(
            "/api/v1/surf-data/Nonexistent%20Beach",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    @patch('app.services.weather_service.WeatherService.get_wind_data')
    @patch('app.services.weather_service.WeatherService.get_wave_data')
    @patch('app.services.weather_service.WeatherService.get_tide_data')
    @patch('app.services.weather_service.WeatherService.get_temperature_data')
    def test_get_surf_data_success(
        self, 
        mock_temp, 
        mock_tide, 
        mock_wave, 
        mock_wind, 
        client, 
        db_session, 
        api_key
    ):
        """Test getting surf data successfully with mocked external APIs"""
        # Mock external API responses
        mock_wind.return_value = {
            "latitude": 39.345894,
            "longitude": -74.41759,
            "hourly": {
                "time": ["2025-01-01T00:00"],
                "wind_speed_10m": [10.0],
                "wind_direction_10m": [180]
            }
        }
        
        mock_wave.return_value = {
            "latitude": 39.345894,
            "longitude": -74.41759,
            "hourly": {
                "time": ["2025-01-01T00:00"],
                "wave_height": [3.0],
                "wave_direction": [90],
                "wave_period": [8.0]
            }
        }
        
        mock_tide.return_value = [
            {"time": "2025-01-01 06:00", "height": "8.5", "type": "high"},
            {"time": "2025-01-01 12:00", "height": "2.1", "type": "low"}
        ]
        
        mock_temp.return_value = {
            "station_id": "test_station",
            "water_temp": "72.5",
            "air_temp": "75.0"
        }
        
        # Create test API key (hash the key for storage)
        key_hash = AuthService.hash_api_key(api_key)
        test_key = APIKey(key_hash=key_hash, name="test_key", is_active=True)
        db_session.add(test_key)
        db_session.commit()
        
        # Create test beach
        test_beach = Beach(
            beach_name="Test Beach",
            town="Test Town",
            state="NJ",
            lat=39.345894,
            long=-74.41759,
            beach_angle=90.0,
            station_id="test_station"
        )
        db_session.add(test_beach)
        db_session.commit()
        
        response = client.get(
            "/api/v1/surf-data/Test%20Beach",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Check response structure
        assert "beach_name" in data
        assert "wind" in data
        assert "waves" in data
        assert "tides" in data
        assert "temperature" in data
        assert "grade" in data
        assert "cached" in data
        
        # Check beach name
        assert data["beach_name"] == "Test Beach"
        
        # Check that external APIs were called
        mock_wind.assert_called_once()
        mock_wave.assert_called_once()
        mock_tide.assert_called_once()
        mock_temp.assert_called_once()
    
    def test_get_surf_data_with_cached_data(self, client, db_session, api_key):
        """Test getting surf data when cached data exists"""
        # Create test API key (hash the key for storage)
        key_hash = AuthService.hash_api_key(api_key)
        test_key = APIKey(key_hash=key_hash, name="test_key", is_active=True)
        db_session.add(test_key)
        db_session.commit()
        
        # Create test beach
        test_beach = Beach(
            beach_name="Test Beach",
            town="Test Town",
            state="NJ",
            lat=39.345894,
            long=-74.41759,
            beach_angle=90.0,
            station_id="test_station"
        )
        db_session.add(test_beach)
        db_session.commit()
        
        # Create cached wind data
        cached_wind = CachedData(
            beach_id=test_beach.id,
            data_type="wind_data",
            data={"test": "wind_data"},
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
        )
        db_session.add(cached_wind)
        
        # Create cached wave data
        cached_wave = CachedData(
            beach_id=test_beach.id,
            data_type="wave_data",
            data={"test": "wave_data"},
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
        )
        db_session.add(cached_wave)
        
        # Create cached tide data
        cached_tide = CachedData(
            beach_id=test_beach.id,
            data_type="tide_data",
            data=[{"test": "tide_data"}],
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
        )
        db_session.add(cached_tide)
        
        # Create cached temperature data
        cached_temp = CachedData(
            beach_id=test_beach.id,
            data_type="temp_data",
            data={"test": "temp_data"},
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
        )
        db_session.add(cached_temp)
        
        db_session.commit()
        
        with patch('app.services.weather_service.WeatherService.get_temperature_data') as mock_temp:
            mock_temp.return_value = {
                "station_id": "test_station",
                "water_temp": "72.5",
                "air_temp": "75.0"
            }
            
            response = client.get(
                "/api/v1/surf-data/Test%20Beach",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            
            # Check that cached data is marked as cached
            assert data["wind"]["cached"] == True
            assert data["waves"]["cached"] == True
            assert data["tides"]["cached"] == True
            assert data["temperature"]["cached"] == True
            
            # Temperature API should NOT be called (cached in this test)
            mock_temp.assert_not_called()
    
    def test_get_surf_data_with_expired_cache(self, client, db_session, api_key):
        """Test getting surf data when cached data is expired"""
        # Create test API key (hash the key for storage)
        key_hash = AuthService.hash_api_key(api_key)
        test_key = APIKey(key_hash=key_hash, name="test_key", is_active=True)
        db_session.add(test_key)
        db_session.commit()
        
        # Create test beach
        test_beach = Beach(
            beach_name="Test Beach",
            town="Test Town",
            state="NJ",
            lat=39.345894,
            long=-74.41759,
            beach_angle=90.0,
            station_id="test_station"
        )
        db_session.add(test_beach)
        db_session.commit()
        
        # Create expired cached data
        expired_wind = CachedData(
            beach_id=test_beach.id,
            data_type="wind_data",
            data={"test": "expired_wind_data"},
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1)  # Expired
        )
        db_session.add(expired_wind)
        db_session.commit()
        
        with patch('app.services.weather_service.WeatherService.get_wind_data') as mock_wind:
            mock_wind.return_value = {
                "latitude": 39.345894,
                "longitude": -74.41759,
                "hourly": {
                    "time": ["2025-01-01T00:00"],
                    "wind_speed_10m": [10.0],
                    "wind_direction_10m": [180]
                }
            }
            
            response = client.get(
                "/api/v1/surf-data/Test%20Beach",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            
            # Should call external API since cache is expired
            mock_wind.assert_called_once() 