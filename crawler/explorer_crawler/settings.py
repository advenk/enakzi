BOT_NAME = 'explorer_crawler'

SPIDER_MODULES = ['explorer_crawler.spiders']
NEWSPIDER_MODULE = 'explorer_crawler.spiders'

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1.0
DEPTH_LIMIT = 3
ITEM_PIPELINES = {
    'explorer_crawler.pipelines.NIMAPipeline': 300,
}
DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'
CONCURRENT_REQUESTS = 16
COOKIES_ENABLED = False
USER_AGENT = 'Mozilla/5.0 (compatible; explorer_crawler/1.0)'
LOG_ENABLED = True
LOG_LEVEL = 'INFO' 