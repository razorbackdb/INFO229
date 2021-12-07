from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Date

import models


def get_news(db: Session, date_from: Date, date_to: Date, category: str):
    response = []
    news = db.query(models.News).filter(models.News.date.between(date_from, date_to)).all()
    for i in news:
        if category in i.categories:
            response.append(i)
    return response