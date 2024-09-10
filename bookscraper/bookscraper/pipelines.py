# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.asdict().keys()  # Retrieve the field names
        
        # strip whitespace:
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                if isinstance(value, list):  # Ensure it's a list before indexing
                    adapter[field_name] = value[0].strip()

        # category & category --> lowercase
        lowercase_fields = ['category', 'subcategory']  # Adjust to use distinct fields
        for lowercase_field in lowercase_fields:
            value = adapter.get(lowercase_field)
            if value:
                adapter[lowercase_field] = value.lower()

        # price --> to float
        price_fields = ['price_excl_tax', 'price_incl_tax', 'tax', 'price']
        for price_field in price_fields:
            value = adapter.get(price_field)
            if value:
                value = value.replace('£', '').strip()
                adapter[price_field] = float(value)

        # availability --> books in stock   
        availability_str = adapter.get('availability')
        if availability_str:
            split_str_list = availability_str.split('(')
            if len(split_str_list) < 2:
                adapter['availability'] = 0
            else:
                split_str_list_2 = split_str_list[1].split()
                adapter['availability'] = int(split_str_list_2[0])

        # num_reviews --> cast to int
        value = adapter.get('num_reviews')
        if value:
            adapter['num_reviews'] = int(value)

        # stars --> to int
        stars_raw = adapter.get('stars')
        if stars_raw:
            stars_str = stars_raw.replace('star-rating', '').strip().lower()
            match(stars_str):
                case 'zero':
                    adapter['stars'] = 0
                case 'one':
                    adapter['stars'] = 1
                case 'two':
                    adapter['stars'] = 2
                case 'three':
                    adapter['stars'] = 3
                case 'four': 
                    adapter['stars'] = 4
                case 'five':
                    adapter['stars'] = 5

        return item


class SaveToMySQLPipeline:

    def __init__(self) -> None:
        # connection
        self.conn = pymysql.connect(
            host='172.17.0.2',
            user='root',
            password='1234', # NO NEED TO HIDE IT FROM YOU, I TRUST YOU :)
            database='books'
        )

        # cursor
        self.cur = self.conn.cursor()

        # create table if not exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment,
            url VARCHAR(255),
            title text,
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            price DECIMAL,
            tax DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute("""
        INSERT INTO books(
            url,
            title, 
            product_type, 
            price_excl_tax, 
            price_incl_tax, 
            price, 
            tax, 
            availability, 
            num_reviews, 
            stars, 
            category, 
            description
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
        item['url'],
        item['title'],
        item['product_type'],
        item['price_excl_tax'],
        item['price_incl_tax'],
        item['price'],
        item['tax'],
        item['availability'],
        item['num_reviews'],
        item['stars'],
        item['category'],
        item['description'],
        ))

        self.conn.commit()
        return item
    
    def close_spider(self, spider):

        # close mariadb connections
        self.cur.close()
        self.conn.close()
        