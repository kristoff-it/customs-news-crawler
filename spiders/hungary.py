# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class HungarySpider(scrapy.Spider):
    name = "hungary"
    allowed_domains = ["police.hu"]
    start_urls = (
        'http://www.police.hu/hirek-es-informaciok/legfrissebb-hireink/bunugyek',
    )


    def parse(self, response):
        for href in response.css("h2 > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_item)
        
        try:
            next_page = response.urljoin(response.css("li.pager-next > a::attr('href')")[0].extract())
            yield scrapy.Request(next_page, callback=self.parse)
        except:
            pass


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css(".field-name-title").xpath('.//text()').extract()[0]
        item['date'] = response.css(".field-name-post-date").xpath('.//text()').extract()[0]
        item['body'] = " ".join(response.css(".field-type-text-long").xpath('.//text()').extract())
        item['link'] = response.url
        item['country'] = 'hungary'
        yield item



