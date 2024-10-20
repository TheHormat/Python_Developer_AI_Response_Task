from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, database
from sqlalchemy import func

router = APIRouter(prefix="/comments", tags=["Comments Analytics"])


@router.get("/daily-breakdown/")
def comments_daily_breakdown(
    date_from: str = Query(...),
    date_to: str = Query(...),
    db: Session = Depends(database.get_db),
):
    try:
        date_from_dt = datetime.strptime(date_from, "%Y-%m-%d")
        date_to_dt = datetime.strptime(date_to, "%Y-%m-%d")

        comments = (
            db.query(models.Comment)
            .filter(
                func.date(models.Comment.created_at)
                >= date_from_dt,  
                func.date(models.Comment.created_at) <= date_to_dt,
            )
            .all()
        )

        return comments
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
