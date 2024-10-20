# For Run:
uvicorn app.main:app --reload

# For Migrations
alembic revision --autogenerate -m "Describe your changes"
alembic upgrade head

# for Tests:
pytest tests/test_post.py
