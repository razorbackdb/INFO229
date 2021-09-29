from typing import List, Optional

from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    date: str
    url: str
    media_outlet: str
    category: str


class NewsCreate(NewsBase):
    pass


class News(NewsBase):
    id: int

    class Config:
        orm_mode = True
