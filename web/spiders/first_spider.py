# -*- coding: utf-8 -*-

import scrapy
from web.items import MovieItem

class first_spider(scrapy.Spider):
    
    name = "first_spider"
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top']
    
    def parse(self, response):
        links = response.xpath('//tbody[@class="lister-list"]/tr/td[@class="titleColumn"]/a/@href').extract()
        print(len(links))
        i = 0
        for link in links:
            abs_url = response.urljoin(link)
            url_next = '//*[@id="main"]/div/span/div/div/div[2]/table/tbody/tr[' +str(i)+']/td[3]/strong/text()'
            rating = response.xpath(url_next).extract()
            i = i + 1
            yield scrapy.Request(abs_url, callback= self.parse_indetail, meta={'rating' : rating})
    
    def parse_indetail(self, response):
        item = MovieItem()
        item['title'] = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract()[0][:-1]
        item['popularity'] = response.xpath('//div[@class="titleReviewBarSubItem"]/div/span/text()').extract()[2][21:-8]
        
        return item
        
        