from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import post, comment, user, analytics

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Routers
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(user.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the homepage!"}