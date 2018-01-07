# -*- coding: utf-8 -*-

BOT_NAME = 'ld_crawler'

SPIDER_MODULES = ['ld_crawler.spiders']
NEWSPIDER_MODULE = 'ld_crawler.spiders'

# USER_AGENT = 'ld_crawler (+http://www.yourdomain.com)'

CONCURRENT_REQUESTS = 32

# DOWNLOAD_DELAY = 3
# COOKIES_ENABLED = False
# TELNETCONSOLE_ENABLED = False

# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

ITEM_PIPELINES = {
   'ld_crawler.pipelines.LdCrawlerPipeline': 300,
}

MONGO_URI = 'mongodb://localhost:27017'
DB_NAME = 'love_defending'
AUTH = {}
