# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


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
