from sqlalchemy import Column, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime
import os
from scrapy import signals
import logging
from datetime import datetime
import math

DeclarativeBase = declarative_base()

class ErrorCallback():
    # error callback for failed scrapy Requests
    def errback(failure, spider):
        ErrorSaving.store_error_in_database(failure, spider, failure.request)

class ErrorSaving():
    #  save all failures to database
    def store_error_in_database(failure, spider, request, response={}):
        if "IS_APP_ENGINE" in os.environ:
            # GAE + Cloud SQL
            engine = create_engine(URL(**spider.settings.get("DATABASE")), pool_pre_ping=True)
        else:
            # LOKAL
            engine = create_engine(URL(**spider.settings.get("DATABASE_DEV")), pool_pre_ping=True)

        session = sessionmaker(bind=engine)()
        DeclarativeBase.metadata.create_all(engine, checkfirst=True)
        e = Error(**{
            "failed_at": datetime.now(),
            "spider": repr(spider),
            "traceback": failure.getTraceback(),
            "request_method": request.method,
            "request_url": request.url,
            "request_meta": json.dumps(request.meta),
            "request_cookies": json.dumps(request.cookies),
            "request_headers": json.dumps(dict(request.headers.to_unicode_dict())),
            "request_body": request.body,
            "response_status": response.status if response else "",
            "response_url": response.url if response else "",
            "response_headers": json.dumps(dict(response.headers.to_unicode_dict())) if response else "",
            "response_body": response.body if response else ""
        })

        try:
            session.add(e)
            session.commit()
        except:
            session.rollback()
            raise

        finally:
            session.close()


class Error(DeclarativeBase):
    __tablename__ = "errors"

    id = Column(Integer, primary_key=True)
    failed_at = Column(DateTime)
    spider = Column(Text(4294000000))
    traceback = Column(Text(4294000000))
    request_method = Column(Text(4294000000))
    request_url = Column(Text(4294000000))
    request_meta = Column(Text(4294000000))
    request_cookies = Column(Text(4294000000))
    request_headers = Column(Text(4294000000))
    request_body = Column(Text(4294000000))
    response_status = Column(Text(4294000000))
    response_url = Column(Text(4294000000))
    response_headers = Column(Text(4294000000))
    response_body = Column(Text(4294000000))


class ErrorSavingMiddleware:
    
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_error, signal=signals.spider_error)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_error(self, failure, response, spider, signal=None, sender=None, *args, **kwargs):
        ErrorSaving.store_error_in_database(failure, spider, response.request, response)

    def spider_opened(self, spider):
        self.start = datetime.now()

    def spider_closed(self, spider, reason):
        elapsed = datetime.now() - self.start
        logging.info("########################################")
        logging.info(f"########## TOTAL RUNTIME: {str(elapsed)}")
        logging.info(f"########## PERFECT GAE SPLITS: {math.ceil(elapsed.total_seconds() / 3600 / 24)}")
        logging.info("########################################")
