import scrapy
from quotescraper.items import QuoteItem
from scrapy_playwright.page import PageMethod
import time # screenshot


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
                PageMethod('wait_for_timeout', 2000),  # Warte Sekunden
                #PageMethod('wait_for_event', 'networkidle'),  # Warte, bis keine Netzwerkanfragen mehr stattfinden
                PageMethod('wait_for_selector', 'div.quote:nth-child(11)'), # doom scroll
            ],
            errback = self.errback
        ))


    async def parse(self, response):

        timestamp = time.strftime('%Y-%m-%dT%H-%M-%S', time.gmtime()) # screenshot
        screenshot_path = f'../zdata/{self.name}/{self.name}_{timestamp}_.png' # screenshot

        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item
            
        page = response.meta["playwright_page"]
        screenshot = await page.screenshot(path = screenshot_path, full_page=True) # screenshot
        await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

# ------------------------------------------------------------------

# import scrapy
# import json

# class QuoteApiSpider(scrapy.Spider):
#     name = "quotes"
#     base_url = "https://quotes.toscrape.com/api/quotes?page="
#     start_page = 1
#     end_page = 10  # Hier stellst du die Anzahl der zu scrapenden Seiten ein

#     def start_requests(self):
#         for page_num in range(self.start_page, self.end_page + 1):
#             url = f"{self.base_url}{page_num}"
#             yield scrapy.Request(url, callback=self.parse_api)

#     def parse_api(self, response):
#         # Lade die JSON-Antwort
#         data = json.loads(response.body)

#         # Extrahiere die Zitate aus der JSON-Antwort
#         for quote in data.get('quotes', []):
#             yield {
#                 'text': quote.get('text'),
#                 'author': quote.get('author', {}).get('name'),
#                 'tags': quote.get('tags', [])
#             }

#         # Überprüfe, ob es eine nächste Seite gibt (falls es mehr als 10 Seiten gibt)
#         if data.get('has_next'):
#             next_page = data.get('page') + 1
#             next_url = f"{self.base_url}{next_page}"
#             yield scrapy.Request(next_url, callback=self.parse_api)

# -----------------------------------------------------------------------------------------------------------

# import scrapy
# from quotescraper.items import QuoteItem
# from scrapy_playwright.page import PageMethod

# class QuoteSpider(scrapy.Spider):
#     name = "quotes"


#     def start_requests(self):
#         url = "http://quotes.toscrape.com/js/"
#         yield scrapy.Request(url, meta=dict(
#             playwright = True,
#             playwright_include_page = True,
#             playwright_page_methods = [
#                 PageMethod('wait_for_selector', 'div.quote'),
#                 PageMethod('evaluate', "window.scrollBy(0, document.body.scrollHeight)"),
#                 PageMethod('wait_for_selector', 'div.quote:nth-child(11)'),
#             ],
#             errback = self.errback
#         ))


#     async def parse(self, response):
#         page = response.meta["playwright_page"]
#         await page.close()

#         for quote in response.css('div.quote'):
#             quote_item = QuoteItem()
#             quote_item['text'] = quote.css('span.text::text').get()
#             quote_item['author'] = quote.css('small.author::text').get()
#             quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
#             yield quote_item

#         next_page = response.css('.next>a ::attr(href)').get()

#         if next_page is not None:
#             next_page_url = 'http://quotes.toscrape.com' + next_page
#             yield scrapy.Request(next_page_url, meta=dict(
#                 playwright = True,
#                 playwright_include_page = True,
#                 playwright_page_methods = [
#                     PageMethod('wait_for_selector', 'div.quote')
#                 ],
#                 errback = self.errback
#             ))


#     async def errback(self, failure):
#         page = failure.request.meta["playwright_page"]
#         await page.close()
