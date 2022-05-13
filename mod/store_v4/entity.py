from sqlalchemy import Integer, SmallInteger, String, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Store(Base):
    __tablename__ = 'tdar_store'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    ctime = Column(DateTime(), default=datetime.now)
    mtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    priority = Column(Integer, default=100)
    comment = Column(String(50))
    is_active = Column(SmallInteger, default=1)
    is_del = Column(SmallInteger, default=0)