# tests/test_auth.py
import json

def test_user_registration(client, db):
    """Test standard user registration succeeds."""
    res = client.post('/api/auth/register', json={
        "username": "testuser",
        "password": "testpassword",
        "role": "Customer"
    })
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data["status"] == "success"
    assert data["user"]["username"] == "testuser"
    assert data["user"]["role"] == "Customer"

def test_user_registration_duplicate(client, db):
    """Test registering a duplicate username fails with 409 conflict."""
    # First registration
    client.post('/api/auth/register', json={
        "username": "testuser",
        "password": "testpassword",
        "role": "Customer"
    })
    # Duplicate registration
    res = client.post('/api/auth/register', json={
        "username": "testuser",
        "password": "anotherpassword",
        "role": "Vendor"
    })
    assert res.status_code == 409
    data = json.loads(res.data)
    assert data["status"] == "error"
    assert "exists" in data["message"]

def test_user_login_success(client, db):
    """Test logging in with correct credentials succeeds."""
    # Register
    client.post('/api/auth/register', json={
        "username": "loginuser",
        "password": "loginpassword",
        "role": "Vendor"
    })
    # Login
    res = client.post('/api/auth/login', json={
        "username": "loginuser",
        "password": "loginpassword"
    })
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["status"] == "success"
    assert data["user"]["username"] == "loginuser"

def test_user_login_failure(client, db):
    """Test logging in with incorrect credentials fails."""
    # Register
    client.post('/api/auth/register', json={
        "username": "loginuser",
        "password": "loginpassword",
        "role": "Vendor"
    })
    # Bad Login
    res = client.post('/api/auth/login', json={
        "username": "loginuser",
        "password": "wrongpassword"
    })
    assert res.status_code == 401
    data = json.loads(res.data)
    assert data["status"] == "error"
