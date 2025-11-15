# \webScrape\newsScraper\newsScraper\pipelines.py

import pymongo 
from scrapy.exceptions import DropItem

class NewsscraperPipeline:
    
    # CRITICAL: These MUST match Django's views.py EXACTLY.
    MONGO_URI = "mongodb://localhost:27017/"
    DB_NAME = 'newsDB'
    COLLECTION_NAME = 'NewsHeadlines_tb'

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        
    def open_spider(self, spider):
        # Establish connection on spider start
        self.client = pymongo.MongoClient(self.MONGO_URI)
        self.db = self.client[self.DB_NAME]
        self.collection = self.db[self.COLLECTION_NAME]
        
    def close_spider(self, spider):
        # Close connection gracefully
        if self.client:
            self.client.close()

    def process_item(self, item, spider):
        item_data = dict(item) 
        
        # Check for duplicates using the unique URL field
        # Using dict(item) ensures the data written is pure Python dict
        if self.collection.count_documents({'url': item_data['url']}, limit=1):
            spider.logger.info(f"Duplicate item found: {item_data['title']}")
            raise DropItem(f"Duplicate item: {item_data['title']}")
        else:
            self.collection.insert_one(item_data)
            spider.logger.info(f"Saved new headline: {item_data['title']}")

        return item