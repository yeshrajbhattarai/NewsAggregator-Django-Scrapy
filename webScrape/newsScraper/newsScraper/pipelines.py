from pymongo import MongoClient
from itemadapter import ItemAdapter
import os
import certifi
from datetime import datetime

class MongoPipeline:
    # CRITICAL FIX: Changed 'NewsHeadlines_tb' to 'headlines' 
    collection_name = 'headlines'
    db_name = 'news_db' 

    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        self.client = None

    @classmethod
    def from_crawler(cls, crawler):
        # Fetches the MONGO_URI from the GitHub Action secret
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
        return cls(mongo_uri=mongo_uri)

    def open_spider(self, spider):
        # Establish the Atlas connection (using certifi for cloud stability)
        try:
            self.client = MongoClient(self.mongo_uri, tlsCAFile=certifi.where())
            self.db = self.client[self.db_name]
            spider.logger.info(f"--- Pipeline: Connected to Mongo Atlas DB: {self.db_name} ---")
        except Exception as e:
            spider.logger.error(f"--- FATAL MONGO DB ERROR: {e} ---")
            self.client = None # Prevents process_item from crashing

    def close_spider(self, spider):
        if self.client:
            self.client.close()

    def process_item(self, item, spider):
        if self.client:
            adapter = ItemAdapter(item)
            
            # The item object MUST have 'url' to prevent duplicates
            if 'url' not in adapter:
                 spider.logger.warning("Item missing 'url' field, skipping.")
                 return item

            # Insert/Update the item based on the link (upsert=True)
            self.db[self.collection_name].update_one(
                {'link': adapter['url']},
                {'$set': {
                    'title': adapter['title'],
                    'link': adapter['url'],
                    'source': adapter.get('source', 'IndianExpress'),
                    'scraped_at': datetime.now() # Add scrape timestamp for sorting
                }},
                upsert=True
            )
        return item