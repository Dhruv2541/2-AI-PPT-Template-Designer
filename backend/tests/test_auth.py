import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "JWT_SECRET_KEY": "test-secret",
        }
    )

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.drop_all()


def test_mock_login(client):
    response = client.post(
        "/api/auth/mock-login", json={"email": "test@example.com", "name": "Test User"}
    )

    assert response.status_code == 200
    data = response.json
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["name"] == "Test User"


def test_get_current_user_unauthorized(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_get_current_user_authorized(client):
    # First login
    login_res = client.post(
        "/api/auth/mock-login", json={"email": "auth@example.com", "name": "Auth User"}
    )
    token = login_res.json["access_token"]

    # Then access protected route
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json["email"] == "auth@example.com"
