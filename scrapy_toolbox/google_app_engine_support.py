#from sqlalchemy import Column, Integer, DateTime, String, Interval
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.engine.url import URL
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#import json
#import os
from scrapy import signals
import logging
from datetime import datetime
import math
# import yaml
import numpy as np

# DeclarativeBase = declarative_base()

class GaePartCalcMiddleware:

#     def __init__(self, settings):
#         engine = self.create_engine()
#         session = self.create_session(engine)
#         create_schema()
#         self.is_app_engine = True if "IS_APP_ENGINE" in os.environ else False

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        #crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        # take first execution time measure point
        self.start = datetime.now()

        if hasattr(spider, 'part') and hasattr(spider, 'number_of_parts'):
            urls = sorted(spider.start_urls)
            parts = np.array_split(urls, int(spider.number_of_parts))
            spider.start_urls = parts[int(spider.part) - 1].tolist()

        # # load number of parts
        # gae_settings = self.get_number_of_parts(spider_name=spider.name, current_timestamp=self.start)
        # if gae_settings:
        #     spider.parts = gae_settings.number_of_parts
        # else:
        #     spider.parts = 1

    def spider_closed(self, spider, reason):
        elapsed = datetime.now() - self.start

#         gae_parts = math.ceil(elapsed.total_seconds() / 3600 * 1,25 * spider.gae_parts / 24)
        logging.info("########################################")
        logging.info(f"########## TOTAL RUNTIME: {str(elapsed)}")
        logging.info(f"########## PERFECT GAE SPLITS: {math.ceil(elapsed.total_seconds() / 3600 / 24)}")
#         logging.info(f"########## OLD NUMBER OF GAE PARTS: {spider.gae_parts}")
#         logging.info(f"########## NEW CALCULATED NUMBER OF GAE PARTS: {gae_parts}")
        logging.info("########################################")

#         # save calculated gae parts to yaml if the scraper is executed locally
#         if "IS_APP_ENGINE" not in os.environ:
#             if os.path.isfile("spider-toolbox.yaml"):
#                 with open("spider-toolbox.yaml", "r") as f:
#                     conf = yaml.safe_load(f)
#                 conf["GAE_PARTS_" + spider.name] = gae_parts
#                 with open("spider-toolbox.yaml", "w+") as f:
#                     yaml.dump(conf, f, default_flow_style=False)
#             else:
#                 conf = {"GAE_PARTS_" + spider.name: gae_parts}
#                 with open("spider-toolbox.yaml", "w+") as f:
#                     yaml.dump(conf, f, default_flow_style=False)

#     def get_number_of_parts(spider_name, current_timestamp):
#         engine = self.create_engine()
#         session = self.create_session(engine)
#         return session.query(__GAE).filter(spider=spider_name).filter(~__GAE.calculated_at.contains(current_timestamp)).order_by(__GAE.calculated_at.desc(), __GAE.parts.desc()).first()

#     def create_engine():
#         if self.is_app_engine:
#             # GAE + Cloud SQL
#             return create_engine(URL(**spider.settings.get("DATABASE")), pool_pre_ping=True)
#         else:
#             # LOKAL
#             return create_engine(URL(**spider.settings.get("DATABASE_DEV")), pool_pre_ping=True)

#     def create_session(engine):
#         return sessionmaker(bind=engine)()

#     def create_schema(engine):
#         DeclarativeBase.metadata.create_all(engine, checkfirst=True)

#     def store_error_in_database(failure, spider, request, response={}):        
        
#         e = __Error(**{
#             "failed_at": datetime.now(),
#             "spider": repr(spider),
#             "traceback": failure.getTraceback(),
#             "request_method": request.method,
#             "request_url": request.url,
#             "request_meta": json.dumps(request.meta),
#             "request_cookies": json.dumps(request.cookies),
#             "request_headers": json.dumps(dict(request.headers.to_unicode_dict())),
#             "request_body": request.body,
#             "response_status": response.status if response else "",
#             "response_url": response.url if response else "",
#             "response_headers": json.dumps(dict(response.headers.to_unicode_dict())) if response else "",
#             "response_body": response.body if response else ""
#         })

#         try:
#             session.add(e)
#             session.commit()
#         except:
#             session.rollback()
#             raise

#         finally:
#             session.close()

# class __GAE(DeclarativeBase):
#     __tablename__ = "__gae"

#     id = Column(Integer, primary_key=True)
#     part = Column(Integer)
#     spider = Column(String(255))
#     runtime = Column(Interval)
#     number_of_parts = Column(Integer)
#     calculated_at = Column(DateTime)
