import pytest
from fastapi import status
from sqlalchemy.orm import Session

from app.models.beach import Beach
from app.models.api_key import APIKey
from app.services.auth_service import AuthService

class TestBeachesEndpoints:
    """Test cases for beaches endpoints"""
    
    def test_get_beaches_without_auth(self, client):
        """Test getting beaches without authentication should fail"""
        response = client.get("/api/v1/beaches/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_beaches_with_invalid_auth(self, client):
        """Test getting beaches with invalid API key should fail"""
        response = client.get(
            "/api/v1/beaches/",
            headers={"Authorization": "Bearer invalid_key"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_beaches_with_valid_auth(self, client, db_session, api_key):
        """Test getting beaches with valid API key"""
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
            "/api/v1/beaches/",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "beaches" in data
        assert len(data["beaches"]) == 1
        assert data["beaches"][0]["beach_name"] == "Test Beach"
    
    def test_get_beach_by_name_not_found(self, client, db_session, api_key):
        """Test getting a beach that doesn't exist"""
        # Create test API key (hash the key for storage)
        key_hash = AuthService.hash_api_key(api_key)
        test_key = APIKey(key_hash=key_hash, name="test_key", is_active=True)
        db_session.add(test_key)
        db_session.commit()
        
        response = client.get(
            "/api/v1/beaches/Nonexistent%20Beach",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_beach_by_name_success(self, client, db_session, api_key):
        """Test getting a specific beach by name"""
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
            "/api/v1/beaches/Test%20Beach",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["beach_name"] == "Test Beach"
        assert data["lat"] == 39.345894
        assert data["long"] == -74.41759
        assert data["state"] == "NJ"
        assert data["town"] == "Test Town"
    
    def test_get_beaches_empty_list(self, client, db_session, api_key):
        """Test getting beaches when none exist"""
        # Create test API key (hash the key for storage)
        key_hash = AuthService.hash_api_key(api_key)
        test_key = APIKey(key_hash=key_hash, name="test_key", is_active=True)
        db_session.add(test_key)
        db_session.commit()
        
        response = client.get(
            "/api/v1/beaches/",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "beaches" in data
        assert len(data["beaches"]) == 0 