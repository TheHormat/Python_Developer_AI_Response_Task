import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app import crud, models, database, schemas

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_test_user(
    test_db: Session, email="testuser@example.com", username="testuser"
):
    user = schemas.UserCreate(email=email, username=username, password="testpassword")
    return crud.create_user(test_db, user)


def create_test_post(test_db: Session, user: models.User):
    post = schemas.PostCreate(title="Test Post", content="This is a test post content")
    return crud.create_post(test_db, post=post, owner_id=user.id)


def authenticate_test_user(client: TestClient, username: str, password: str) -> str:
    response = client.post(
        "/users/login/", data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json().get("access_token")


def test_create_comment(test_db: Session):
    user = create_test_user(
        test_db, email="uniqueuser@example.com", username="uniqueuser"
    )
    token = authenticate_test_user(client, "uniqueuser", "testpassword")
    post = create_test_post(test_db, user=user)

    response = client.post(
        f"/posts/{post.id}/comments/",
        json={"content": "This is a test comment", "auto_reply_enabled": False},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "This is a test comment"
    assert data["post_id"] == post.id
    assert data["owner_id"] == user.id


def test_read_comments(test_db: Session):
    user = create_test_user(
        test_db, email="uniqueuser2@example.com", username="uniqueuser2"
    )
    token = authenticate_test_user(client, "uniqueuser2", "testpassword")
    post = create_test_post(test_db, user=user)

    client.post(
        f"/posts/{post.id}/comments/",
        json={"content": "Another test comment", "auto_reply_enabled": False},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get(
        f"/posts/{post.id}/comments/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) > 0 


def test_delete_comment(test_db: Session):
    user = create_test_user(
        test_db, email="uniqueuser3@example.com", username="uniqueuser3"
    )
    token = authenticate_test_user(client, "uniqueuser3", "testpassword")
    post = create_test_post(test_db, user=user)

    comment_response = client.post(
        f"/posts/{post.id}/comments/",
        json={"content": "Comment to delete", "auto_reply_enabled": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    comment_id = comment_response.json()["id"]

    delete_response = client.delete(
        f"/posts/{post.id}/comments/{comment_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Comment deleted successfully"
