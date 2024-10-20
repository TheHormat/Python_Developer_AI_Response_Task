## For Run:
```bash
  poetry shell
  poetry install
  poetry update

  uvicorn app.main:app --reload
```

## For Migrations
```bash
  alembic revision --autogenerate -m "Describe your changes"
  alembic upgrade head
```

## for Tests:
```bash
  pytest tests/test_post.py
```
