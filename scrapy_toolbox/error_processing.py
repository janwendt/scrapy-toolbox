from scrapy import signals
from .error_handling import Error

class ErrorProcessingMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        if hasattr(spider, 'process_errors'):
            session = spider.crawler.database_session
            errors = session.query(Error).all()
            spider.start_urls = list({error.url for error in errors})
            session.query(Error).delete(synchronize_session=False)
            session.commit()
