from urllib.parse import urlencode
import scrapy
import json
import re



class IndeedSpider(scrapy.Spider):
    name = "indeed_jobs"

    # allowed_domains = ["de.indeed.com"]
    # start_urls = ["https://de.indeed.com/jobs"]

    def get_indeed_search_url(self, keyword, location, offset=0):
        parameters= {"q": keyword, "l": location, "filter": 0, "start": offset} # "from": searchOnHP, 
        return "https://de.indeed.com/jobs?" + urlencode(parameters)
    

    def start_requests(self):
        keyword_list = ['Fachinformatiker', 'Anwendungsentwicklung']
        location_list = ['Frankfurt']
        for keyword in keyword_list:
            for location in location_list:
                indeed_jobs_url = self.get_indeed_search_url(keyword, location)
                yield scrapy.Request(url=indeed_jobs_url, callback=self.parse_search_results, meta={'keyword': keyword, 'location': location, 'offset': 0})

    def parse_search_results(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword'] 
        offset = response.meta['offset'] 
        script_tag  = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
        
            # Paginate Through Jobs Pages
            if offset == 0:
                meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"]
                num_results = sum(category["jobCount"] for category in meta_data)
                if num_results > 1000:
                    num_results = 50
                
                for offset in range(10, num_results + 10, 10):
                    url = self.get_indeed_search_url(keyword, location, offset)
                    yield scrapy.Request(url=url, callback=self.parse_search_results, meta={'keyword': keyword, 'location': location, 'offset': offset})
    