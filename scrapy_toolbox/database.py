from scrapy import signals
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import os

# import logging
# logger = logging.getLogger(__name__)

DeclarativeBase = declarative_base()

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabasePipeline(object):
    __metaclass__ = Singleton

    def __init__(self, settings):
        self.database = settings.get("DATABASE")
        self.database_dev = settings.get("DATABASE_DEV")
        self.session = self.get_session()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        crawler.database_session = pipeline.session
        return pipeline

    def get_session(self):
        engine = self.create_engine()
        self.create_tables(engine)
        return self.create_session(engine)

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

    def spider_closed(self, spider):
        self.session.close()
