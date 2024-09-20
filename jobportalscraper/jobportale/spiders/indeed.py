from scrapy.http import Response
from jobportale.items import JobportaleItem
from urllib.parse import urlencode
import scrapy
import json
import re


class IndeedSpider(scrapy.Spider):
    name = "indeed_jobs"
    allowed_domains = ["de.indeed.com"]
    # start_urls = ["https://de.indeed.com/jobs"]
    start_urls = ["https://de.indeed.com/jobs?q=fachinformatiker+anwendungsentwicklung&l=Frankfurt"]


    custom_settings = {
    'DOWNLOAD_DELAY': 3,  # Verzögert Anfragen um 3 Sekunden
    }

    def start_requests(self):
        # Es wird über die Liste `start_urls` iteriert und jede URL einzeln gesendet
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={'playwright': True, 'playwright_page_methods': [
                    {'method': 'wait_for_timeout', 'args': [3000]}  # Warte 3 Sekunden, bevor die Seite geparst wird
                ]},
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
            )

    def parse(self, response):
            # Extrahieren von Jobanzeigen aus der HTML-Struktur
            job_listings = response.css('div.job_seen_beacon')  # CSS-Selektor anpassen, falls nötig
            self.logger.info(f"Seite geladen: {response.url}")
            
            for job in job_listings:
                # Extrahieren der Jobdaten
                item = JobportaleItem()
                item['job_titel'] = job.css('h2.jobTitle span::text').get()
                item['firma'] = job.css('span[data-testid="company-name"]::text').get()
                item['ort'] = job.css('div[data-testid="text-location"]::text').get()
                item['meta_daten'] = job.css('div.underShelfFooter li::text').getall()
                item['url_portal'] = response.urljoin(job.css('a::attr(href)').get())
                item['geschaltet'] = job.css('span[data-testid="myJobsStateDate"]::text').get()
                
                # Jobdaten ausgeben
                yield item

            # Paginierung: Weiter zu den nächsten Seiten
            next_page = response.css('a[aria-label="Weiter"]::attr(href)').get()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse, meta={'playwright': True})
