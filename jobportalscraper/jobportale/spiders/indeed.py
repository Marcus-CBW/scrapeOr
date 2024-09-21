from jobportale.items import JobportaleItem
from urllib.parse import urlencode
import scrapy, random, time


class IndeedSpider(scrapy.Spider):
    name = "indeed_jobs"
    allowed_domains = ["de.indeed.com"]
    schlagworte = {
        'q': 'fachinformatiker anwendungsentwicklung',
        'l': 'Frankfurt',
        'radius': 50
    }
    anfrage = urlencode(schlagworte)
    start_urls = [f"https://de.indeed.com/jobs?{anfrage}"]

    custom_settings = {
        'DOWNLOAD_DELAY': 6,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': False,
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    'playwright': True,
                    'playwright_context': 'persistent',
                },
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
            )

    def parse(self, response):
        # Extrahieren von Jobanzeigen aus der HTML-Struktur
        job_listings = response.css('div.job_seen_beacon')  # CSS-Selektor anpassen, falls nötig
        self.logger.info(f"Seite geladen: {response.url}")
        
        for job in job_listings:
            # Extrahieren der Jobdaten
            item = JobportaleItem()
            item['job_titel'] = job.css('h2.jobTitle span::text').get(default='N/A')
            item['firma'] = job.css('span[data-testid="company-name"]::text').get(default='N/A')
            item['ort'] = job.css('div[data-testid="text-location"]::text').get(default='N/A')
            item['meta_daten'] = job.css('div.underShelfFooter li::text').getall()
            item['url_portal'] = response.urljoin(job.css('a::attr(href)').get(default=''))
            item['geschaltet'] = job.css('span[data-testid="myJobsStateDate"]::text').get(default='N/A')
            
            # Jobdaten ausgeben
            yield item

        # Paginierung: Weiter zu den nächsten Seiten
        next_page = response.css('a[data-testid="pagination-page-next"]::attr(href)').get()
        if next_page:

            # Zufällige Verzögerung einfügen
            delay = random.uniform(4, 6)
            self.logger.info(f"Warte {delay} Sekunden, bevor die nächste Seite geladen wird.")
            time.sleep(delay)

            # Wenn ein Link zur nächsten Seite gefunden wird, erfolgt die nächste Anfrage
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse,
                meta={
                    'playwright': True,
                    'playwright_context': 'persistent',
                    'playwright_headless': False,
                    'playwright_page_methods': [{
                        'method': 'wait_for_timeout',
                        'args': [3000]
                    }]
                },
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
            )
        else:
            # Loggen, wenn keine nächste Seite gefunden wurde
            self.logger.info('Keine weiteren Seiten gefunden.')
