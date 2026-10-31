from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint contract and response."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_predict_endpoint_valid():
    """Test prediction endpoint with valid input data (Positive case)."""
    payload = {"feature1": 6.0, "feature2": 5.0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert data["prediction"] == 1

def test_predict_endpoint_edge_case():
    """Test prediction endpoint edge case (Negative prediction)."""
    payload = {"feature1": 2.0, "feature2": 3.0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == 0

def test_predict_invalid_schema():
    """Test input validation schema with missing/invalid types."""
    payload = {"feature1": "invalid_string", "feature2": 5.0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (Pydantic validation error)

def test_api_contract_headers():
    """Test API contract and content-type headers."""
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"