import scrapy
from chocolatescraper.items import ChocolateProduct
from chocolatescraper.itemloaders import ChocolateProductLoader

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://chocolate.co.uk/collections/all"]

    # def parse(self, response):
    #     pass
    def parse(self, response):

        products = response.css('product-item')

        product_item = ChocolateProduct()
        for product in products:

            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            chocolate.add_css('name', 'a.product-item-meta__title::text'),
            #chocolate.add_css('price', 'span.price', re=r'(\d{1,5}(?:,\d{3})*\.\d{2})')
            chocolate.add_css('price', 'span.price', re=r'<span class="visually-hidden">(.*?)\s*(\d{1,5}(?:,\d{3})*(?:\.\d{2})?)')
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)') # ::attr(href) selektiert das href-Attribut der a-Tags, 
            # d.h., es extrahiert den Link (URL), der mit dem href-Attribut verbunden ist.
            yield chocolate.load_item()

        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(next_page_url, callback=self.parse)
