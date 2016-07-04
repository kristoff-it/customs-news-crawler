# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class MontenegroSpider(scrapy.Spider):
    name = "montenegro"
    allowed_domains = ["upravacarina.gov.me"]
    start_urls = ['http://www.upravacarina.gov.me/en/news?pagerIndex={}'.format(i) for i in range(1, 4)]


    def parse(self, response):
        for href in response.css(".mainContent2 > .section > h2 > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_item)


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css(".mainContent3 > h2").xpath('.//text()').extract()[0]
        item['date'] = "".join(response.css(".mainContent3 > .detalji-hold > .detalji").xpath('.//text()').extract()).strip()
        item['body'] = " ".join(response.css(".mainContent3").xpath('.//text()').extract())
        item['link'] = response.url
        item['country'] = 'montenegro'
        yield item



