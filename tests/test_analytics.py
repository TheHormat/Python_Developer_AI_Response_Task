import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
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


def authenticate_test_user(client, username, password):
    response = client.post(
        "/users/login/", data={"username": username, "password": password}
    )
    return response.json().get("access_token")


def test_comments_daily_breakdown(test_db: Session):
    # Test kullanıcı oluşturuluyor
    user = create_test_user(
        test_db, email="uniqueuser@example.com", username="uniqueuser"
    )

    token = authenticate_test_user(client, "uniqueuser", "testpassword")

    post = create_test_post(test_db, user=user)

    for i in range(3):
        response = client.post(
            f"/posts/{post.id}/comments/",
            json={"content": f"Test Comment {i+1}", "auto_reply_enabled": False},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

    date_from = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
    date_to = datetime.utcnow().strftime("%Y-%m-%d")

    response = client.get(
        f"/comments/daily-breakdown/?date_from={date_from}&date_to={date_to}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) == 3
