# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class BulgariaSpider(scrapy.Spider):
    name = "bulgaria"
    allowed_domains = ["customs.bg"]
    start_urls = ['http://customs.bg/bg/pubs/0?p={}'.format(i) for i in range(416)]

    def parse(self, response):
        for href in response.css('.news > p > a::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_item)
        
        # try:
        #     next_page = response.urljoin(response.css('.pager-next > a::attr(href)')[0].extract())
        #     yield scrapy.Request(next_page, callback=self.parse)
        # except:
        #     pass


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css('.news > h3').xpath('.//text()').extract()[0]
        item['date'] = response.css('.news > i').xpath('.//text()').extract()[0]
        item['body'] = " ".join(response.css('.news').xpath('.//text()').extract())
        item['link'] = response.url
        item['country'] = 'bulgaria'
        yield item



