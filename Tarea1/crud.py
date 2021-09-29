from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import and_, Date

from . import models, schemas


def get_news(db: Session, date_from: Date, date_to: Date, category: str):
    return db.query(models.News).filter(and_(models.News.between(date_from, date_to), models.News.categories == category)).all()
