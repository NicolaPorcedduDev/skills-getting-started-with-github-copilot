import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data
    assert "participants" in data["Soccer Team"]

def test_signup_success():
    response = client.post("/activities/Art%20Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Art Club" in response.json()["message"]
    # Try again, should fail (already signed up)
    response2 = client.post("/activities/Art%20Club/signup?email=testuser@mergington.edu")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
