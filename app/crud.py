from sqlalchemy.orm import Session
from app import models, schemas, utils
from datetime import datetime
from sqlalchemy import func


# User
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# Post
def create_post(db: Session, post: schemas.PostCreate, owner_id: int):
    db_post = models.Post(**post.model_dump(), owner_id=owner_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()


def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# Comment
def create_comment(
    db: Session, comment: schemas.CommentCreate, post_id: int, owner: models.User
):
    db_comment = models.Comment(
        content=comment.content,
        post_id=post_id,
        owner_id=owner.id,  
        is_blocked=utils.contains_profanity(comment.content),
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db: Session, post_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Comment)
        .filter(models.Comment.post_id == post_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_comment(db: Session, comment_id: int):
    db_comment = (
        db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment


def get_comments_daily_breakdown(
    db: Session, post_id: int, date_from: str, date_to: str
):
    try:
        date_from_dt = datetime.strptime(date_from, "%Y-%m-%d")
        date_to_dt = datetime.strptime(date_to, "%Y-%m-%d")

        results = (
            db.query(
                func.date(models.Comment.created_at).label("date"),
                func.count(models.Comment.id).label("total_comments"),
            )
            .filter(
                models.Comment.post_id == post_id,
                func.date(models.Comment.created_at)
                >= date_from_dt,
                func.date(models.Comment.created_at) <= date_to_dt,
            )
            .group_by(func.date(models.Comment.created_at))
            .all()
        )
        return results
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")
