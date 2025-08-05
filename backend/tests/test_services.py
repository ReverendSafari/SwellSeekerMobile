import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta

from app.services.grading_service import GradingService
from app.services.cache_service import CacheService
from app.services.auth_service import AuthService
from app.models.beach import Beach
from app.models.api_key import APIKey
from app.models.cached_data import CachedData

class TestGradingService:
    """Test cases for the grading service"""
    
    def test_grade_surf_conditions_green(self):
        """Test grading for good surf conditions"""
        wind_data = {
            "hourly": {
                "wind_speed_10m": [8.0, 9.0, 10.0],
                "wind_direction_10m": [270, 275, 280]  # Offshore wind
            }
        }
        
        wave_data = {
            "hourly": {
                "wave_height": [4.0, 5.0, 6.0],
                "wave_period": [12.0, 13.0, 14.0],
                "wave_direction": [90, 95, 100]
            }
        }
        
        grade = GradingService.calculate_grade_from_data(wind_data, wave_data, 90.0)
        assert grade == "yellow"
    
    def test_grade_surf_conditions_yellow(self):
        """Test grading for moderate surf conditions"""
        wind_data = {
            "hourly": {
                "wind_speed_10m": [12.0, 15.0, 18.0],
                "wind_direction_10m": [180, 185, 190]  # Cross-shore wind
            }
        }
        
        wave_data = {
            "hourly": {
                "wave_height": [2.0, 3.0, 4.0],
                "wave_period": [8.0, 9.0, 10.0],
                "wave_direction": [90, 95, 100]
            }
        }
        
        grade = GradingService.calculate_grade_from_data(wind_data, wave_data, 90.0)
        assert grade == "red"
    
    def test_grade_surf_conditions_red(self):
        """Test grading for poor surf conditions"""
        wind_data = {
            "hourly": {
                "wind_speed_10m": [25.0, 30.0, 35.0],
                "wind_direction_10m": [180, 185, 190]
            }
        }
        
        wave_data = {
            "hourly": {
                "wave_height": [1.0, 1.5, 2.0],
                "wave_period": [5.0, 6.0, 7.0],
                "wave_direction": [90, 95, 100]
            }
        }
        
        grade = GradingService.calculate_grade_from_data(wind_data, wave_data, 90.0)
        assert grade == "red"

class TestCacheService:
    """Test cases for the cache service"""
    
    def test_store_and_get_cached_data(self, db_session):
        """Test storing and retrieving cached data"""
        # Create test beach
        beach = Beach(
            beach_name="Test Beach",
            town="Test Town",
            state="NJ",
            lat=39.345894,
            long=-74.41759,
            beach_angle=90.0,
            station_id="test_station"
        )
        db_session.add(beach)
        db_session.commit()
        
        # Test data
        test_data = {"test": "data"}
        
        # Store data
        CacheService.store_cached_data(db_session, beach.id, "test_type", test_data)
        
        # Retrieve data
        cached_data = CacheService.get_cached_data(db_session, beach.id, "test_type")
        
        assert cached_data is not None
        assert cached_data["data"] == test_data
        assert cached_data["cached"] == True
    
    def test_get_cached_data_not_found(self, db_session):
        """Test getting cached data that doesn't exist"""
        cached_data = CacheService.get_cached_data(db_session, 999, "test_type")
        assert cached_data is None
    
    def test_get_cached_data_expired(self, db_session):
        """Test getting expired cached data"""
        # Create test beach
        beach = Beach(
            beach_name="Test Beach",
            town="Test Town",
            state="NJ",
            lat=39.345894,
            long=-74.41759,
            beach_angle=90.0,
            station_id="test_station"
        )
        db_session.add(beach)
        db_session.commit()
        
        # Create expired cached data
        expired_data = CachedData(
            beach_id=beach.id,
            data_type="test_type",
            data={"test": "expired_data"},
            expires_at=datetime.now(timezone.utc) - timedelta(hours=1)
        )
        db_session.add(expired_data)
        db_session.commit()
        
        # Try to get expired data
        cached_data = CacheService.get_cached_data(db_session, beach.id, "test_type")
        assert cached_data is None
    
    def test_store_cached_data_replaces_existing(self, db_session):
        """Test that storing new data replaces existing data"""
        # Create test beach
        beach = Beach(
            beach_name="Test Beach",
            town="Test Town",
            state="NJ",
            lat=39.345894,
            long=-74.41759,
            beach_angle=90.0,
            station_id="test_station"
        )
        db_session.add(beach)
        db_session.commit()
        
        # Store initial data
        initial_data = {"test": "initial_data"}
        CacheService.store_cached_data(db_session, beach.id, "test_type", initial_data)
        
        # Store new data
        new_data = {"test": "new_data"}
        CacheService.store_cached_data(db_session, beach.id, "test_type", new_data)
        
        # Retrieve data
        cached_data = CacheService.get_cached_data(db_session, beach.id, "test_type")
        
        assert cached_data["data"] == new_data
        assert cached_data["data"] != initial_data

class TestAuthService:
    """Test cases for the authentication service"""
    
    def test_validate_api_key_valid(self, db_session):
        """Test validating a valid API key"""
        # Create test API key
        test_key = "test_key_123"
        key_hash = AuthService.hash_api_key(test_key)
        api_key = APIKey(key_hash=key_hash, name="test_key", is_active=True)
        db_session.add(api_key)
        db_session.commit()
        
        # Validate API key
        is_valid = AuthService.validate_api_key(db_session, test_key)
        assert is_valid == True
    
    def test_validate_api_key_invalid(self, db_session):
        """Test validating an invalid API key"""
        is_valid = AuthService.validate_api_key(db_session, "invalid_key")
        assert is_valid == False
    
    def test_validate_api_key_inactive(self, db_session):
        """Test validating an inactive API key"""
        # Create inactive API key
        test_key = "inactive_key"
        key_hash = AuthService.hash_api_key(test_key)
        api_key = APIKey(key_hash=key_hash, name="inactive_key", is_active=False)
        db_session.add(api_key)
        db_session.commit()
        
        # Validate API key
        is_valid = AuthService.validate_api_key(db_session, test_key)
        assert is_valid == False
    
    def test_validate_api_key_nonexistent(self, db_session):
        """Test validating a non-existent API key"""
        is_valid = AuthService.validate_api_key(db_session, "nonexistent_key")
        assert is_valid == False 