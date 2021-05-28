# Scrapy settings for family project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'family'

SPIDER_MODULES = ['family.spiders']
NEWSPIDER_MODULE = 'family.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'family (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'family.middlewares.FamilySpiderMiddleware': 543,
#}
SPIDER_MIDDLEWARES = {
    'scrapy_toolbox.database.DatabasePipeline': 999,
    'scrapy_toolbox.error_handling.ErrorSavingMiddleware': 1000,
    'scrapy_toolbox.error_processing.ErrorProcessingMiddleware': 1000,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'family.middlewares.FamilyDownloaderMiddleware': 543,
#}
# DOWNLOADER_MIDDLEWARES = {
#     # The priority of 560 is important, because we want this middleware to kick in just before the scrapy built-in `RetryMiddleware`.
#     'scrapy_cloudflare_middleware.middlewares.CloudFlareMiddleware': 560
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'family.pipelines.FamilyPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DATABASE = {
    'drivername': 'mysql+pymysql',
    'username': '...',
    'password': '...',
    'database': 'family',
    'host': '...',
    'port': '3306'
}

DATABASE_DEV = {
    'drivername': 'mysql+pymysql',
    'username': '...',
    'password': '...',
    'database': 'family',
    'host': '127.0.0.1',
    'port': '3306'
}

# Set to True if you want to automatically send Mails when an Error occurs 
SEND_MAILS = False
MAIL_HOST = "..."
MAIL_FROM = "..."
MAIL_TO = "..."

# Set to True if you want to automatically create GitHub Issue when an Error occurs 
CREATE_GITHUB_ISSUE = False
GITHUB_TOKEN = "..."
GITHUB_REPO = "janwendt/scrapy-toolbox"
