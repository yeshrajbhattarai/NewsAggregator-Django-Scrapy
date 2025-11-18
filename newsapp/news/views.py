from django.shortcuts import render
from django.conf import settings 

def index(request):
    # 1. Define the collection name (Must match Scrapy)
    COLLECTION_NAME = 'headlines'
    
    news_items = []
    
    try:
        # 2. Use the global DB connection from settings.py
        collection = settings.db[COLLECTION_NAME]
        
        # 3. Fetch data (sorted by newest first)
        news_items = list(collection.find().sort("scraped_at", -1).limit(25))
        print(f"DEBUG: Found {len(news_items)} items.")
        
    except Exception as e:
        print(f"DATABASE ERROR: {e}")

    context = {'headlines': news_items}
    return render(request, 'index.html', context)