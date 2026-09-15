"""Tests for API endpoints"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_status_endpoint():
    """Test status endpoint"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AI Trading Room"
    assert "version" in data
    assert "docs" in data

def test_api_v1_agents_list():
    """Test agents list endpoint"""
    response = client.get("/api/v1/agents/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_api_v1_portfolio_stats():
    """Test portfolio stats endpoint"""
    response = client.get("/api/v1/portfolio/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_equity" in data
    assert "cash" in data

def test_api_v1_risk_status():
    """Test risk status endpoint"""
    response = client.get("/api/v1/risk/status")
    assert response.status_code == 200
    data = response.json()
    assert "kill_switch" in data
    assert "exposure" in data
