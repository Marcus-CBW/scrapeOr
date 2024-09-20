from scrapy.http import Response
from jobportale.items import JobportaleItem
from urllib.parse import urlencode
import scrapy
import json
import re


class IndeedSpider(scrapy.Spider):
    name = "indeed_jobs"
    allowed_domains = ["de.indeed.com"]
    start_urls = ["https://de.indeed.com/jobs"]

    def start_requests(self):
        url = start_urls
        yield scrapy.Request(url, meta={'playwright': True})

    def parse(self, response):
        pass

