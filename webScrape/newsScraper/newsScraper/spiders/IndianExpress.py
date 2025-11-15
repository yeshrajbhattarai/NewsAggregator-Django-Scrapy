# \webScrape\newsScraper\newsScraper\spiders\IndianExpress.py

import scrapy
from ..items import NewsscraperItem # Correct relative import

class IndianexpressSpider(scrapy.Spider):
    name = "IndianExpress"
    allowed_domains = ["indianexpress.com"]
    start_urls = ["https://indianexpress.com/"]

    def parse(self, response):
        # Selector remains consistent
        headline_selectors = response.css('h3 a[data-vr-excerpttitle]')
        
        for selector in headline_selectors:
            title = selector.css('::text').get() 
            link = selector.css('::attr(href)').get()
            
            if title and link:
                item = NewsscraperItem()
                
                # Strip whitespace and set the source name
                item['title'] = title.strip()
                item['url'] = link.strip()
                item['source'] = self.name # 'IndianExpress'
                
                yield item