from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database, utils

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=schemas.PostOut)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(utils.get_current_user),
):
    if utils.contains_profanity(post.content):
        raise HTTPException(status_code=400, detail="Post contains prohibited language")
    return crud.create_post(db=db, post=post, owner_id=current_user.id)


@router.get("/")
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(database.get_db)):
    db_post = crud.delete_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
