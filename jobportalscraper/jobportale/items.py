# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobportaleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_titel = scrapy.Field()
    firma = scrapy.Field()
    ort = scrapy.Field()
    meta_daten = scrapy.Field()
    url_portal = scrapy.Field()
    url_firma = scrapy.Field()
    geschaltet = scrapy.Field()
    
#https://de.indeed.com/jobs?q=Fachinformatiker+Anwendungsentwicklung&l=Frankfurt+am+Main&from=searchOnHP
