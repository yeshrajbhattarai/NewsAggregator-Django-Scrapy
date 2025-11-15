import scrapy


class NdtvscraperSpider(scrapy.Spider):
    name = "BBCScraper"
    allowed_domains = ["www.news.google.com"]
    start_urls = ["https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRE55YXpBU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen"]

    def parse(self, response):
        headline = response.css("a.XlKvRb::text").getall()
        titles = response.css('h3 a::text').getall()
        if headline:
            for title in headline:
                yield {
                    "headline": title.strip(),
                    "title": titles
                    }
        else:
            print("No headlines found on the page.")
                
