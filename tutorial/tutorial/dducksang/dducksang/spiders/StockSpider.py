import scrapy

class StockSpider(scrapy.Spider):
    name = "stock"

    def start_requests(self):
        urls = [
            'http://gall.dcinside.com/board/view/?id=stock_new2&no=3008576&page=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('td.t_subject'):
            text = quote.css("a::text").extract()
            if text is None or text == "" :  
                text = quote.css("a b").extract()
            print(text)

