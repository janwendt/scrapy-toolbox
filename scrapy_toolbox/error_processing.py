from scrapy import signals

class ErrorProcessingMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        print("###############ERROR_PROCESSING")
        if hasattr(spider, 'process_errors'):
            print("ERROR_PROCESSING1")
            session = spider.dbPipeline.sessions[self]
            session.query(models.Market.id, models.Market.zip_code).all() # limit(5) für Testzwecke
            spider.start_urls = parts[int(spider.part) - 1].tolist()
        else:
            print("ERROR_PROCESSING2")
        
