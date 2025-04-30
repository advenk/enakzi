import scrapy

class ExplorerItem(scrapy.Item):
    image_url = scrapy.Field()
    source_url = scrapy.Field()
    caption = scrapy.Field()
    hash = scrapy.Field()
    score = scrapy.Field()
    url = scrapy.Field() 