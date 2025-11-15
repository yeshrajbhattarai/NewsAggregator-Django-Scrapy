# \webScrape\newsScraper\newsScraper\items.py

import scrapy

class NewsscraperItem(scrapy.Item):
    # These fields MUST match what is saved to MongoDB
    title = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()