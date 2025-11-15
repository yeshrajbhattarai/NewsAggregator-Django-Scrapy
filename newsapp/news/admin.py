from django.contrib import admin
from .models import Headline  # Import your model

# Use the decorator to register the model
@admin.register(Headline)
class HeadlineAdmin(admin.ModelAdmin):
    # Optional: Customize how the data looks in the admin list view
    list_display = ('title', 'source', 'url') 
    # Optional: Add a search bar
    search_fields = ('title', 'source') 
    # Optional: Make the list clickable by title
    list_display_links = ('title',)