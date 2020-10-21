scrapy-toolbox
=============

A Python library that extends Scrapy with the following features:
- Support for Google App Engine (GAE): Bypass Google App Engines 24 hour execution time limit (https://cloud.google.com/appengine/docs/standard/go/how-instances-are-managed#scaling_types) by dividing the start_urls into x parts
- Error Saving to the Database Table "errors" for manual error analysis (incl. traceback and response) and automated request reconstruction containing the following columns:
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

Requisites: 
-----------

* settings.py with a dict for DATABASE_DEV and DATABASE

Installation
------------

  ```
  pip install scrapy-toolbox
  ```

Setup
-----

Add `scrapy_toolbox.error_handling.ErrorSavingMiddleware` and `scrapy_toolbox.google_app_engine_support.GaePartCalcMiddleware` extensions to your Scrapy Project `settings.py`.

Example:

  ```
  # settings.py
  SPIDER_MIDDLEWARES = {
      'scrapy_toolbox.error_handling.ErrorSavingMiddleware': 1000,
      'scrapy_toolbox.google_app_engine_support.GaePartCalcMiddleware': 1000,
  }

  ```

Usage
-----

  - The ErrorSavingMiddleware defines a errback Callback for your Requests. So if you want to make use of this Feature do not define any errback.
  - To split the start_urls into x parts just start your spider by adding the two arguments `part` and `number_of_parts` where part is the part which should be executed during this run and number_of_parts defines the number of parts that exist in total. So if you want to split your start_urls into 3 Parts:
```
  scrapy crawl test -a part=1 -a number_of_parts=3
  scrapy crawl test -a part=2 -a number_of_parts=3
  scrapy crawl test -a part=3 -a number_of_parts=3
```

Supported versions
------------------
This package works with Python 3. It has been tested with Scrapy up to version 1.4.0.

Tasklist
------------------
- [] Process Errors from your Database Table "errors" at a later time and execute failed Request: for instance when the website was down or you got an Exception during parsing for specific requests and want to crawl them again
- [] Automatic Part calculation and saving in DB??? 
