import scrapy


class CrackmesSpider(scrapy.Spider):
    MAX_PAGE = 78 # 78
    BASE_URL = "https://crackmes.one/"
    
    current_page = 1
    name = "crackmes"
    start_urls = ["https://crackmes.one/lasts/1"]
        
    def parse(self, response):
        crackmes_list = response.css("tr.text-center")
        for crackme in crackmes_list:
            relative_detail_page = crackme.css("td:nth-child(1) a::attr(href)").get()
            detail_page = self.BASE_URL + relative_detail_page
            
            crackmeItem = {
                'title': crackme.css('td:nth-child(1) a::text').get(),
                'author': crackme.css('td:nth-child(2) a::text').get(),
                'language': crackme.css('td:nth-child(3)::text').get(),
                'architecture': crackme.css('td:nth-child(4)::text').get(),
                'difficulty': crackme.css('td:nth-child(5)::text').get(),
                'quality': crackme.css('td:nth-child(6)::text').get(),
                'platform': crackme.css('td:nth-child(7)::text').get(),
                'date': crackme.css('td:nth-child(8)::text').get(),
                'solutions': crackme.css('td:nth-child(9)::text').get(),
                'comments': crackme.css('td:nth-child(10)::text').get(),
            }
            
            yield scrapy.Request(detail_page, callback=self.parse_detail_page, meta={'item': crackmeItem})
        
        if(self.current_page < self.MAX_PAGE):
            self.current_page += 1
            next_page_url = self.BASE_URL + "lasts/" + str(self.current_page)
            yield response.follow(next_page_url, callback=self.parse)
        
        
    def parse_detail_page(self, response):
        item = response.meta['item']
        item['download_url'] = self.BASE_URL + response.css("div.col-2 a::attr(href)").get()
        item['description'] = response.css("div.col-12 span::text").get()
        
        yield item
            