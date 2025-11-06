from scrapy import signals
from .error_handling import Error
from scrapy import Request
import json

class ErrorProcessingMiddleware:
    def process_start(self, start_requests, spider):
        print("process_start_requests")
        if hasattr(spider, 'process_errors'):
            session = spider.crawler.database_session
            errors = session.query(Error).all()
            requests = []
            for error in errors:
                meta = json.loads(error.request_meta)
                del meta["download_latency"]
                req = Request(
                    url = error.url,
                    method = error.request_method,
                    meta = meta,
                    body = error.request_body,
                    headers = json.loads(error.request_headers),
                    cookies = json.loads(error.request_cookies),
                    dont_filter = True,
                )
                if not any([req.__dict__ == r.__dict__ for r in requests]):
                    requests.append(req)
            session.query(Error).delete(synchronize_session=False)
            session.commit()
            yield from requests            
        else:
            yield from start_requests
