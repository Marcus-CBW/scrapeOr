import scrapy
from quotescraper.items import QuoteItem
from scrapy_playwright.page import PageMethod
import time

class QuoteSpider(scrapy.Spider):
    name = "quotes"


    def start_requests(self):
        url = "http://quotes.toscrape.com/scroll"
        yield scrapy.Request(url, meta=dict(
            playwright = True,
            playwright_include_page = True,
            playwright_page_methods = [
                PageMethod('wait_for_selector', 'div.quote'),
                PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"), # doom scroll
                PageMethod('wait_for_event', 'response', lambda response: response.status == 200 and 'application/json' in response.headers.get('content-type')),
                # ↑ wartet auf eine beliebige Netzwerkantwort, die den Statuscode 200 und den Inhaltstyp application/json hat, und ist etwas allgemeiner als die ursprüngliche Überprüfung auf quotes?page=
                # PageMethod('wait_for_response', lambda response: 'quotes?page=' in response.url and response.status == 200 and 'application/json' in response.headers.get('content-type')),
                PageMethod('wait_for_timeout', 2000),  # Warte...
                #PageMethod('wait_for_event', 'networkidle'),  # Warte, bis keine Netzwerkanfragen mehr stattfinden
                PageMethod('wait_for_selector', 'div.quote:nth-child(11)'), # doom scroll
            ],
            errback = self.errback
        ))


    async def parse(self, response):

        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item
            
        page = response.meta["playwright_page"]
        
        timestamp = time.strftime('%Y-%m-%dT%H-%M-%S', time.gmtime()) # screenshot
        screenshot_path = f'../zdata/{self.name}/{self.name}_{timestamp}_.png' # screenshot
        screenshot = await page.screenshot(path = screenshot_path, full_page=True) # screenshot

        await page.close()


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

