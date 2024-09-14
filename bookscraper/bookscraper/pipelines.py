# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        return item

import mysql.connector

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class BookscraperPipeline:
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
        self.create_table()

    def create_connection(self):
        try:
            #import pdb; pdb.set_trace()

            self.connection = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = '',
                database = 'book_scraping',
                port = '3306'
            )
            self.curr = self.connection.cursor()
            print("Connection established.")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def create_table(self):
        try:
            # Check if the table exists by querying information_schema
            self.curr.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables 
                WHERE table_schema = %s
                AND table_name = %s
            """, ('book_scraping', 'book_products'))
            table_exists = self.curr.fetchone()[0]

            if table_exists:
                print("Table already exists.")
            else:
                # Create table if it doesn't exist
                self.curr.execute("""
                    CREATE TABLE book_products (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        price DECIMAL(10, 2) NULL,
                        url VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.connection.commit()
                print("Table created.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
       
        try:
            # Use item.get() to handle missing 'price' key
            price = item.get('price', None)  # If 'price' doesn't exist, use None
            
            # Insert into database with the possibly None price value
            self.curr.execute("""
                INSERT INTO book_products (name, price, url) 
                VALUES (%s, %s, %s)
            """, (item['name'], price, item['url']))
            
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
