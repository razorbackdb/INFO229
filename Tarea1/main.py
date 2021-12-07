from typing import List
from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/news", response_model=List[schemas.News])
def read_news(date_from: date, date_to: date, category: str, db: Session = Depends(get_db)):
    news = crud.get_news(db, date_from=date_from, category=category, date_to=date_to)
    return news