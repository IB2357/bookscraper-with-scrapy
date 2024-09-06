import scrapy


class SimplebookspiderSpider(scrapy.Spider):
    name = "simplebookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            yield{
                'title': book.css('h3 a').attrib['title'],
                'price': book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a').attrib['href']
            }
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            # the old way
            # if 'catalogue/' in next_page:
            #     next_page_url = "https://books.toscrape.com/"+next_page
            # else:
            #     next_page_url = "https://books.toscrape.com/"+next_page
            next_page_url = response.urljoin(next_page) # this handels reletive routs perfectly
            yield response.follow(next_page_url, callback=self.parse)