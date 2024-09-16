import scrapy
from scrapy import Spider
from scrapy.http import FormRequest
from http import cookies


class asic_login_spider(Spider):
    name = "basic_login_spider"


    def start_requests(self):
        url = "http://quotes.toscrape.com/login"
        yield scrapy.Request(url, callback = self.login)


    def login(self, response):
        token = response.css("from input[name=csrf_token]::attr(value)").extract_first()
        yield FormRequest.from_response(response, formdata = {
            
                'ssrf_token': token,
                'password': 'foobar',
                'username': 'foobar'},
                callback=self.start_scraping
            )
        

    def start_scraping(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small-author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
