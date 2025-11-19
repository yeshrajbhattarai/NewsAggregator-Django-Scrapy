from django.shortcuts import render
from django.conf import settings 

def index(request):
    COLLECTION_NAME = 'headlines'
    news_items = []
    
    try:
        # FIX: Changed 'settings.db' to 'settings.MONGO_DB' to match settings.py
        collection = settings.MONGO_DB[COLLECTION_NAME]
        
        # Fetch data: sorted by newest first
        news_items = list(collection.find().sort("scraped_at", -1).limit(25))
        print(f"DEBUG: Found {len(news_items)} items.")
        
    except AttributeError:
        print("CRITICAL ERROR: settings.MONGO_DB not found. Check settings.py")
    except Exception as e:
        print(f"DATABASE ERROR: {e}")

    context = {'headlines': news_items}
    return render(request, 'index.html', context)
