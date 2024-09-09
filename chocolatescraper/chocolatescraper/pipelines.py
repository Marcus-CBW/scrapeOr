# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
from mysql.connector import Error

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class ChocolatescraperPipeline:
    def process_item(self, item, spider):
        return item

class PriceToUSDPipeline:
    gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('price'):

            floatPrice = float(adapter['price'])

            adapter['price'] = floatPrice * self.gbpToUsdRate

            return item
        
        else:
            raise DropItem(f"Missing price in {item}")

class DuplicatesPipeline:

    def __init__(self):
        self.names_seen = set()

    def proccess_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter['name'] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter['name'])
            return item
        
class SavingToMysqlPipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'chocolate_scraping',
            port = '3306'
        )
        self.curr = self.connection.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        try:
            self.curr.execute("""INSERT INTO chocolate_products (name, price, url) VALUES (%s, %s, %s)""", (
                # item["name"],
                # item["price"],
                # item["url"]

                item.get("name", "Unknown Name"),  # Default to "Unknown Name" if name is missing
                item.get("price", None),  # Default to None if price is missing
                item.get("url", "Unknown URL")  # Default to "Unknown URL" if URL is missing
            
            ))
            self.connection.commit()
            print("Data inserted successfully!")
            
        except BaseException as e:
            print(e)

