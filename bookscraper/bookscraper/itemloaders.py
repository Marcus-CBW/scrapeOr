
from email.policy import default
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst

class BookProductLoader(ItemLoader):

    default_output_processor = TakeFirst()
    price_in = MapCompose(
        lambda x: x.strip(),  # Remove leading/trailing whitespace
        lambda x : x.split("£")[-1],
        float
        )

    url_in = MapCompose(
        #lambda x: x.replace('../', ''),  # Remove '../'
        lambda x : 'https://books.toscrape.com/catalogue/' + x.replace('../', '')
        )
