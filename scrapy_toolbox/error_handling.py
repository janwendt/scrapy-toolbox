from scrapy import signals
from sqlalchemy import Column, Integer, DateTime, Text, String
from .database import DeclarativeBase
from datetime import datetime
import json
from functools import wraps
import inspect
import traceback
from smtplib import SMTP
from email.message import EmailMessage
from os import path as ospath
from scrapy.utils.project import get_project_settings
from git import Repo
from github import Github
from pathlib import Path
from itertools import chain
import sys
import re

settings = get_project_settings()

def except_hook(exctype, value, tb):
    issue = create_github_issue(exctype, value, tb)
    send_mail(exctype, value, tb, issue)
    sys.__excepthook__(exctype, value, tb)
sys.excepthook = except_hook

class ErrorSaving():
    def store_error_in_database(failure, spider, request, response={}, item_error=False):
        print("#####################################################store_error_in_database")
        request.meta.pop("loader", None)
        e = Error(**{
            "failed_at": datetime.now(),
            "spider": spider.name,
            "traceback": failure.getTraceback(),
            "url": request.meta["splash"]["args"]["url"] if "splash" in request.meta else request.url, # done
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
        session = spider.crawler.database_session
        try:
            session.add(e)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

class Error(DeclarativeBase):
    __tablename__ = "__errors"

    id = Column(Integer, primary_key=True)
    failed_at = Column(DateTime)
    spider = Column(String(255))
    traceback = Column(Text)
    url = Column(Text)
    request_method = Column(String(7))
    request_url = Column(Text)
    request_meta = Column(Text)
    request_cookies = Column(Text)
    request_headers = Column(Text)
    request_body = Column(Text)
    response_status = Column(String(4))
    response_url = Column(Text)
    response_headers = Column(Text)
    response_body = Column(Text)


class ErrorSavingMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_error, signal=signals.spider_error)
        crawler.signals.connect(s.request_scheduled, signal=signals.request_scheduled)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.item_error, signal=signals.item_error)
        crawler.signals.connect(s.item_dropped, signal=signals.item_dropped)
        return s

    # Parse callback Exceptions
    def spider_error(self, failure, response, spider, signal=None, sender=None, *args, **kwargs): 
        print("#####################################################spider_error")
        issue = create_github_issue(failure.type, failure.value, failure.tb)
        send_mail(failure.type, failure.value, failure.tb, issue)
        ErrorSaving.store_error_in_database(failure, spider, response.request, response)

    # Request Exceptions: 502 Bad Gateway, 500, 404
    def request_scheduled(self, request, spider):
        if not request.errback:
            request.errback = lambda failure: ErrorSaving.store_error_in_database(failure, spider, failure.request, failure.value.response if hasattr(failure.value, 'response') else {})

    def process_spider_exception(self, response, exception, spider):
        print("#####################################################process_spider_exception")

    def process_exception(self, request, exception, spider):
        print("#####################################################process_exception")

    def spider_closed(self, spider, reason):
        print("#####################################################spider_closed")

    # Pipeline Exceptions
    def item_error(self, item, response, spider, failure):
        print("#####################################################item_error")
        issue = create_github_issue(failure.type, failure.value, failure.tb)
        send_mail(failure.type, failure.value, failure.tb, issue)
        ErrorSaving.store_error_in_database(failure, spider, response.request, response, item_error=True)

    def item_dropped(self, item, response, exception, spider):
       print("#####################################################item_dropped")

def create_github_issue(exctype, value, tb):
    if settings["CREATE_GITHUB_ISSUE"]:
        create_new_issue = True
        identifier = f'<!---\n{"".join(traceback.format_exception(exctype, value, tb, limit=-1))}\n-->'
        g = Github(settings["GITHUB_TOKEN"])
        repo = g.get_repo(settings["GITHUB_REPO"])
        issues = repo.get_issues(state='open')
        for i in issues:
            if identifier in i.body:
                create_new_issue = False
                match = re.search("Occurences: [0-9]+", i.body, flags=re.IGNORECASE)
                occurences = int(match.group(0).split()[1]) + 1
                i.edit(body = re.sub("Occurences: [0-9]+", f"Occurences: {occurences}", i.body, flags=re.IGNORECASE))
                return None
        if create_new_issue:
            title=f"{settings.get('BOT_NAME')}:{sys.argv[1]} | {value}"
            trace = "".join(traceback.format_exception(exctype, value, tb))
            issue = repo.create_issue(
                title=title,
                body=f"Scraper: {settings.get('BOT_NAME')}\nSpider: {sys.argv[1]}\nPath: {ospath.join(ospath.join(ospath.realpath(sys.argv[1]), 'spiders'), f'{sys.argv[1]}.py')}\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nOccurences: 1\n```{trace}```\n\n{identifier}",
                labels=[repo.get_label("bug")])
            return issue.number
    else:
        return None

def send_mail(exctype, value, tb, issue):
    if settings["SEND_MAILS"]:
        trace = "".join(traceback.format_exception(exctype, value, tb))
        msg = EmailMessage()
        content = f"Project: {ospath.basename(Repo('.', search_parent_directories=True).working_tree_dir)}\nScraper: {settings.get('BOT_NAME')}\nSpider: {sys.argv[1]}\n"
        if issue:
            msg.set_content(f"{content}Github Issue: https://github.com/{settings['GITHUB_REPO']}/issues/{issue}\n\n{trace}")
        else:
            msg.set_content(f"{content}\n{trace}")
        msg["Subject"] = f"Error in Project: {ospath.basename(Repo('.', search_parent_directories=True).working_tree_dir)}, Scraper: {settings.get('BOT_NAME')}, Spider: {sys.argv[1]}"
        msg["From"] = settings["MAIL_FROM"]
        msg["To"] = settings["MAIL_TO"]
        s = SMTP(settings["MAIL_HOST"])
        s.send_message(msg)
        s.quit()

def catch_exception(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            f = func(self, *args, **kwargs)
            if inspect.isgenerator(f):
                value = next(f)
                return chain([value], f)
            else:
                return f
        except StopIteration:
            return f
        except Exception as e:
            issue = create_github_issue(type(e), e, e.__traceback__)
            send_mail(type(e), e, e.__traceback__, issue)
            raise
    return wrapper

class ErrorCatcher(type):
    def __new__(cls, name, bases, dct):
        for m in dct:
            if hasattr(dct[m], '__call__'):
                dct[m] = catch_exception(dct[m])
        return type.__new__(cls, name, bases, dct)
