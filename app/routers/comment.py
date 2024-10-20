from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app import crud, schemas, database, utils, models
from app.routers.ai_response import (
    generate_ai_response,
)
import time

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])


@router.post("/", response_model=schemas.CommentOut)
def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(utils.get_current_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    db_comment = crud.create_comment(
        db=db, comment=comment, post_id=post_id, owner=current_user
    )

    if comment.auto_reply_enabled:
        background_tasks.add_task(auto_reply_comment, db_comment.content)

    return db_comment


def auto_reply_comment(comment_content: str):
    time.sleep(5)
    ai_response = generate_ai_response(comment_content)
    print(f"AI Response: {ai_response}")


@router.get("/")
def read_comments(
    post_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)
):
    return crud.get_comments(db, post_id=post_id, skip=skip, limit=limit)


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(database.get_db)):
    db_comment = crud.delete_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
