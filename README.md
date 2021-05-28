scrapy-toolbox
=============

A Python library that extends Scrapy with the following features:
- Error Saving to the Database Table "__errors" for manual error analysis (incl. traceback and response) and automated request reconstruction containing the following columns:
  - failed_at
  - spider
  - traceback
  - url (original url)
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
- Mapper to automaticaly map scrapy.Item on a database-object  
- Mail Notification when an Exception occurs (HTTP Errors (404, 502, ...) are excluded and only stored in the Database)
- Automatic GitHub Issue creation when an Exception occurs (HTTP Errors (404, 502, ...) are excluded and only stored in the Database)

Requisites: 
-----------

* Environment variable "PRODUCTION" for Produciton Mode for instance in your Dockerfile
* The ErrorSavingMiddleware defines an errback Callback for your Requests. If you want to make use of this Feature do not define any errback.

Installation
------------

  ```
  pip install --upgrade scrapy-toolbox
  ```

Example Project
------------
You can find an example project [here](example/).

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

  CREATE_GITHUB_ISSUE = True # Toggle GitHub Issue creation
  GITHUB_TOKEN = "..."
  GITHUB_REPO = "janwendt/scrapy-toolbox" # for instance

  SEND_MAILS = True # Toggle Mail Notification
  MAIL_HOST = "..."
  MAIL_FROM = "..."
  MAIL_TO = "..."
  ```

Usage
-----
Spider (Import ErrorCatcher first!!!):
  ```
  from scrapy_toolbox.error_handling import ErrorCatcher
  import scrapy
  ...

  class XyzSpider(scrapy.Spider, metaclass=ErrorCatcher):
  ...
  ```

Database Pipeline:
  ```
  # pipelines.py
  from scrapy_toolbox.database import DatabasePipeline
  import xy.items as items
  import xy.model as model

  class ScraperXYZPipeline(DatabasePipeline):
        def __init__(self, settings):
          super().__init__(settings, items, model)
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

Limitations
------------------
Syntax Errors in your settings.py are not handled.

Supported versions
------------------
This package works with Python 3. It has been tested with Scrapy up to version 1.4.0.

Tasklist
------------------
- [] Error Processing
- [] Scaffold for instance ItemPipeline

Build Realease
------------------
```
python setup.py sdist bdist_wheel
cd dist
pip install --upgrade --no-deps --force-reinstall scrapy_toolbox-0.3.3-py3-none-any.whl
cd ..
twine upload dist/*
```
