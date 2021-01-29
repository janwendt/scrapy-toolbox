scrapy-toolbox
=============

A Python library that extends Scrapy with the following features:
- Error Saving to the Database Table "__errors" for manual error analysis (incl. traceback and response) and automated request reconstruction containing the following columns:
  - failed_at
  - spider
  - traceback
  - request_method
  - request_url
  - request_meta (json dump that can be loaded with json.loads())
  - request_cookies (json dump that can be loaded with json.loads())
  - request_headers (json dump that can be loaded with json.loads())
  - request_body
  - response_status
  - response_url
  - response_headers (json dump that can be loaded with json.loads())
  - response_body
- Error Processing with request reconstruction
- DatabasePipeline for SQLAlchemy

Requisites: 
-----------

* Environment variable "PRODUCTION" for Produciton Mode for instance in your Dockerfile
* The ErrorSavingMiddleware defines a errback Callback for your Requests. If you want to make use of this Feature do not define any errback.

Installation
------------

  ```
  pip install --upgrade scrapy-toolbox
  ```

Setup
-----

Add the scrapy_toolbox Middlewares to your Scrapy Project `settings.py` and set your DATABASE_DEV and DATABASE.

  ```
  # settings.py
  SPIDER_MIDDLEWARES = {
      'scrapy_toolbox.database.DatabasePipeline': 999,
      'scrapy_toolbox.error_handling.ErrorSavingMiddleware': 1000,
      'scrapy_toolbox.error_processing.ErrorProcessingMiddleware': 1000,
  }

  # Example when using a MySQL
  DATABASE = {
    'drivername': 'mysql+pymysql', 
    'username': '...',
    'password': '...',
    'database': '...',
    'host': '...',
    'port': '3306'
  }

  DATABASE_DEV = {
      'drivername': 'mysql+pymysql',
      'username': '...',
      'password': '...',
      'database': '...',
      'host': '127.0.0.1',
      'port': '3306'
  }

  ```

Usage
-----
Database Pipeline:
  ```
  # pipelines.py
  from scrapy_toolbox.database import DatabasePipeline

  class ScraperXYZPipeline(DatabasePipeline):
    def process_item(self, item, spider):
        ...
  ```

  ```
  # models.py
  import scrapy_toolbox.database as db

  # then use db.DeclarativeBase as your declarative base
  class Car(db.DeclarativeBase):
    ...
  ```

Query Data:
  ```
  # spiderXYZ.py
  session = self.crawler.database_session
  session.query(models.Market.id, models.Market.zip_code).all()
  ```

Process Errors:
  ```
  scrapy crawl spider_xyz -a process_errors=True
  ```

Supported versions
------------------
This package works with Python 3. It has been tested with Scrapy up to version 1.4.0.

Tasklist
------------------
- [] Process Errors from your Database Table "errors" at a later time and execute failed Request: for instance when the website was down or you got an Exception during parsing for specific requests and want to crawl them again

Build Realease
------------------
```
python setup.py sdist bdist_wheel
twine upload dist/*
```
