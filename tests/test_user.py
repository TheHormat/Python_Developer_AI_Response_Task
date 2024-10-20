import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app import crud, database, schemas

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_register(test_db: Session):
    response = client.post(
        "/users/register/",
        json={
            "email": "simpleuser@example.com",
            "username": "simpleuser",
            "password": "simplepassword",
        },
    )

    assert response.status_code == 201  
    data = response.json()
    assert data["email"] == "simpleuser@example.com"
    assert data["username"] == "simpleuser"


def test_login(test_db: Session):
    user = schemas.UserCreate(
        email="loginuser@example.com", username="loginuser", password="loginpassword"
    )
    crud.create_user(db=test_db, user=user)

    response = client.post(
        "/users/login/", data={"username": "loginuser", "password": "loginpassword"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
