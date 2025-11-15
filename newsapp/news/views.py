# \newsapp\news\views.py

from django.shortcuts import render, HttpResponse 
import pymongo
from pymongo.errors import ConnectionFailure

# Function to render the landing page (assuming it exists)
from django.shortcuts import render
import pymongo

def index(request):
    # 1. Setup MongoDB Connection
    MONGO_URI = "mongodb://localhost:27017/"
    DB_NAME = 'newsDB'
    COLLECTION_NAME = 'NewsHeadlines_tb'
    
    news_items = []
    client = None

    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # 2. Fetch Data (sorted by newest)
        news_items = list(collection.find().sort('_id', -1).limit(25))
        
        # Debugging
        print(f"DEBUG: Found {len(news_items)} items for the home page.")

    except Exception as e:
        print(f"DEBUG: Error connecting to DB: {e}")

    finally:
        if client:
            client.close()

    # 3. Pass data to the template
    context = {
        'headlines': news_items, 
    }
    
    # Make sure this matches your template filename (e.g., 'head.html' or 'index.html')
    return render(request, 'index.html', context)
