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


def create_test_user(test_db: Session):
    user_data = schemas.UserCreate(
        email="testuser@example.com", username="testuser", password="testpassword"
    )
    return crud.create_user(test_db, user_data)


def authenticate_test_user(client: TestClient, username: str, password: str) -> str:
    response = client.post(
        "/users/login/", data={"username": username, "password": password}
    )
    assert response.status_code == 200  
    return response.json().get("access_token")


def test_create_post(test_db: Session):
    user = create_test_user(test_db)
    token = authenticate_test_user(client, "testuser", "testpassword")

    response = client.post(
        "/posts/",
        json={"title": "Test Post", "content": "This is a test post content"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post content"
    assert data["owner_id"] == user.id


def test_read_posts(test_db: Session):
    user = create_test_user(test_db)
    token = authenticate_test_user(client, "testuser", "testpassword")

    response = client.get("/posts/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0


def test_delete_post(test_db: Session):
    user = create_test_user(test_db)
    token = authenticate_test_user(client, "testuser", "testpassword")

    post_response = client.post(
        "/posts/",
        json={"title": "Post to delete", "content": "This post will be deleted"},
        headers={"Authorization": f"Bearer {token}"},
    )
    post_id = post_response.json()["id"]

    delete_response = client.delete(
        f"/posts/{post_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Post deleted successfully"
