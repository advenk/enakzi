BOT_NAME = 'archillect_crawler'

SPIDER_MODULES = ['archillect_crawler.spiders']
NEWSPIDER_MODULE = 'archillect_crawler.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1.0

# Limit how deep we go from the seed URLs
DEPTH_LIMIT = 10

# Default item pipeline
ITEM_PIPELINES = {
    'archillect_crawler.pipelines.NIMAPipeline': 300,
}

# Respect duplicates (Scrapy's built-in duplications)
DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'

# Additional settings for better crawling
CONCURRENT_REQUESTS = 16
COOKIES_ENABLED = False
USER_AGENT = 'Mozilla/5.0 (compatible; ArchillectBot/1.0)'

# Enable logging
LOG_ENABLED = True
LOG_LEVEL = 'INFO' 