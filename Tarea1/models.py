from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base #Se importa el objeto Base desde el archivo database.py


has_category = Table('association', Base.metadata,
    Column('news_id', ForeignKey('news.id'), primary_key=True),
    Column('categories_id', ForeignKey('categories.id'), primary_key=True)
)

class News(Base): 

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, index=True)
    date = Column(Date, unique=True, index=True)
    url = Column(String(50), unique=True, index=True)
    media_outlet = Column(String(50), unique=True, index=True)

    categories = relationship("Categories", secondary=has_category)

class Categories(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(50), unique=True, index=True)
