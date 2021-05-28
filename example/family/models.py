import scrapy_toolbox.database as db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Mother(db.DeclarativeBase):
    __tablename__ = "mothers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    # You only need to add this if you want to query the relationship in one of your spiders. It does not affect your Database Schema.
    children = relationship("Child")

class Child(db.DeclarativeBase):
    __tablename__ = "childs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mother_id = Column(Integer, ForeignKey("mothers.id"), primary_key=True)
    name = Column(String(255))
