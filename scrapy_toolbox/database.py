from scrapy import signals
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from .mapper import ItemsModelMapper
import os

DeclarativeBase = declarative_base()

# https://www.python.org/download/releases/2.2/descrintro/#__new__
class Singleton(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it
    def init(self, *args, **kwds):
        pass

class DatabasePipeline(Singleton):
    def __init__(self, settings, items=None, model=None, database=None, database_dev=None):
        if database:
            self.database = database
        else:
            self.database = settings.get("DATABASE")
        if database_dev:
            self.database_dev = database_dev
        else:
            self.database_dev = settings.get("DATABASE_DEV")
        self.session = self.get_session()
        if items and models:
            self.mapper = self.create_mapper(items, model)

    def create_mapper(self, items, model):
        return ItemsModelMapper(items=items, model=model)

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

    def process_item(self, item, spider):
        obj = self.mapper.map_to_model(item = item, sess = self.session)
        try:
            self.session.add(obj)
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return item

