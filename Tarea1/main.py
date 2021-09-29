from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, Date

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/news/{news_id}", response_model=List[schemas.News])
def read_news(date_from: Date, date_to: Date, category: str, db: Session = Depends(get_db)):
    news = crud.get_news(db, date_from=date_from, category=category, date_to=date_to)
    return news