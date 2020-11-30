from scrapy import signals
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
import os

DeclarativeBase = declarative_base()

class DatabasePipeline(object):
    def __init__(self, settings):
        self.database = settings.get("DATABASE")
        self.database_dev = settings.get("DATABASE_DEV")
        self.sessions = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def create_engine(self):
        if "PRODUCTION" in os.environ:
            engine = create_engine(URL(**self.database))
        else:
            engine = create_engine(URL(**self.database_dev))
        if not database_exists(engine.url):
            create_database(engine.url)
        return engine

    def create_tables(self, engine):
        DeclarativeBase.metadata.create_all(engine, checkfirst=True)

    def create_session(self, engine):
        session = sessionmaker(bind=engine, autoflush=False)() # autoflush=False: "This is useful when initializing a series of objects which involve existing database queries, where the uncompleted object should not yet be flushed." for instance when using the Association Object Pattern
        return session

    def spider_opened(self, spider):
        engine = self.create_engine()
        self.create_tables(engine)
        session = self.create_session(engine)
        self.sessions[spider] = session

    def spider_closed(self, spider):
        session = self.sessions.pop(spider)
        session.close()
