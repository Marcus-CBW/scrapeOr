import scrapy
from bookscraper.items import BookProduct
from bookscraper.itemloaders import BookProductLoader

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books_1/"]

    # Initialize the item counter
    item_count = 0
    max_items = 42  # Set the maximum number of items to scrape, None to scrape all

    # Overwrites FEEDS configuration in settings.py
    # custom_settings = {
    #     'FEEDS':    {'../data/%(name)s/%(name)s_%(mtime)s.csv': {'format': 'csv',}}
    #     }
    

    def parse(self, response):

        products = response.css('article.product_pod')

        for product in products:

            # Check if we've reached the max_items limit
            if self.max_items is not None and self.item_count >= self.max_items:
                return  # Stop the spider once we've scraped enough items
            
            book = BookProductLoader(item=BookProduct(), selector=product)
            book.add_css('name', 'article.product_pod h3 a::attr(title)'),
            book.add_css('price', 'p.price_color::text'),
            book.add_css('url', 'article.product_pod h3 a::attr(href)')

            # my_item = book.load_item()
            # print("my_item debugg: ", my_item['url'])

            self.item_count += 1 

            yield book.load_item()

        next_page = response.css('li.next a::attr(href)').get()

        #if next_page is not None:
        #if next_page is not None and item_count < max_items:
        if next_page and (self.max_items is None or self.item_count < self.max_items):

            next_page_url = self.start_urls[0] + next_page
            yield response.follow(next_page_url, callback = self.parse)
