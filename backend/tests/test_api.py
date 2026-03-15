"""
============================================
TEST_API.PY
Test the Flask API endpoints

Run:
    cd backend
    python -m tests.test_api
============================================
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.app import create_app


def get_test_client():
    """Create a test client"""
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_health_check():
    """Test the health check endpoint"""

    print("\n🧪 Test 1: Health Check (GET /)")
    print("-" * 40)

    client = get_test_client()
    response = client.get("/")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "running"

    print(f"   Status: {response.status_code}")
    print(f"   Response: {data}")
    print("   ✅ Passed!")


def test_api_health():
    """Test API health endpoint"""

    print("\n🧪 Test 2: API Health (GET /api/health)")
    print("-" * 40)

    client = get_test_client()
    response = client.get("/api/health")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"

    print(f"   Status: {response.status_code}")
    print(f"   Response: {data}")
    print("   ✅ Passed!")


def test_scan_safe_url():
    """Test scanning a safe URL"""

    print("\n🧪 Test 3: Scan Safe URL (POST /api/scan)")
    print("-" * 40)

    client = get_test_client()
    response = client.post(
        "/api/scan",
        data=json.dumps({"url": "https://www.google.com"}),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] == True
    assert "phishing_score" in data
    assert "risk_level" in data
    assert "reasons" in data

    print(f"   URL: https://www.google.com")
    print(f"   Score: {data['phishing_score']}")
    print(f"   Risk: {data['risk_level']}")
    print(f"   Reasons: {data['reasons']}")
    print("   ✅ Passed!")


def test_scan_phishing_url():
    """Test scanning a phishing URL"""

    print("\n🧪 Test 4: Scan Phishing URL (POST /api/scan)")
    print("-" * 40)

    client = get_test_client()
    phishing_url = "http://192.168.1.1/login/bank-secure/verify.php"

    response = client.post(
        "/api/scan",
        data=json.dumps({"url": phishing_url}),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] == True
    assert data["phishing_score"] > 40  # Should be suspicious or phishing

    print(f"   URL: {phishing_url}")
    print(f"   Score: {data['phishing_score']}")
    print(f"   Risk: {data['risk_level']}")
    print(f"   Reasons: {len(data['reasons'])} reasons found")
    print("   ✅ Passed!")


def test_scan_no_url():
    """Test scanning without providing URL"""

    print("\n🧪 Test 5: No URL Provided (POST /api/scan)")
    print("-" * 40)

    client = get_test_client()
    response = client.post(
        "/api/scan",
        data=json.dumps({}),
        content_type="application/json"
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] == False

    print(f"   Status: {response.status_code}")
    print(f"   Error: {data['error']}")
    print("   ✅ Passed!")


def test_scan_empty_url():
    """Test scanning with empty URL"""

    print("\n🧪 Test 6: Empty URL (POST /api/scan)")
    print("-" * 40)

    client = get_test_client()
    response = client.post(
        "/api/scan",
        data=json.dumps({"url": ""}),
        content_type="application/json"
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] == False

    print(f"   Status: {response.status_code}")
    print(f"   Error: {data['error']}")
    print("   ✅ Passed!")


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Running API Tests")
    print("=" * 50)

    test_health_check()
    test_api_health()
    test_scan_safe_url()
    test_scan_phishing_url()
    test_scan_no_url()
    test_scan_empty_url()

    print("\n" + "=" * 50)
    print("✅ All API tests passed!")
    print("=" * 50)