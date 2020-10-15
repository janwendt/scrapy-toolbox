scrapy-toolbox
=============

Saves Scrapy exceptions in a Database


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

Add `scrapy_toolbox.errorhandling.ErrorSavingMiddleware` extension to your Scrapy Project `settings.py`.

Example:

  ```
  # settings.py
  SPIDER_MIDDLEWARES = {
      'scrapy_toolbox.error_handling.ErrorSavingMiddleware': 1000,
  }

  ```

Supported versions
------------------
This package works with Python 3. It has been tested with Scrapy up to version 1.4.0.