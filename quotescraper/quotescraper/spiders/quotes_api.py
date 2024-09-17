import scrapy
import json

class QuoteApiSpider(scrapy.Spider):
    name = "quotes_api"
    base_url = "https://quotes.toscrape.com/api/quotes?page="
    start_page = 1
    end_page = 10  # Hier stellst du die Anzahl der zu scrapenden Seiten ein

    def start_requests(self):
        for page_num in range(self.start_page, self.end_page + 1):
            url = f"{self.base_url}{page_num}"
            yield scrapy.Request(url, callback=self.parse_api)

    def parse_api(self, response):
        # Lade die JSON-Antwort
        data = json.loads(response.body)

        # Extrahiere die Zitate aus der JSON-Antwort
        for quote in data.get('quotes', []):
            yield {
                'text': quote.get('text'),
                'author': quote.get('author', {}).get('name'),
                'tags': quote.get('tags', [])
            }

        # Überprüfe, ob es eine nächste Seite gibt (falls es mehr als 10 Seiten gibt)
        if data.get('has_next'):
            next_page = data.get('page') + 1
            next_url = f"{self.base_url}{next_page}"
            yield scrapy.Request(next_url, callback=self.parse_api)
