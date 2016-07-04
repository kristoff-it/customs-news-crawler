# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class KosovoSpider(scrapy.Spider):
    name = "kosovo"
    allowed_domains = ["rks-gov.net"]
    start_urls = ['https://dogana.rks-gov.net/en/News/page/{}'.format(i) for i in range(1, 25)]


    def parse(self, response):
        for href in response.css(".news-ul > li > a::attr('href')"):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_item)


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css(".news-open > div > div > h1").xpath('.//text()').extract()[0]
        item['date'] = response.css(".news-open > div > div > h5").xpath('.//text()').extract()[0]
        item['body'] = " ".join(response.css(".news-open > div").xpath('.//text()').extract())
        item['link'] = response.url
        item['country'] = 'kosovo'
        yield item



