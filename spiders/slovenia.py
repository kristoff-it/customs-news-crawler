# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class SloveniaSpider(scrapy.Spider):
    name = "slovenia"
    allowed_domains = ["fu.gov.si"]
    start_urls = (
        'http://www.fu.gov.si/carina/?tx_news_pi1%5Barchived%5D=1&tx_news_pi1%5Bmore%5D=1&cHash=8f566678aa1be231efafc07ec0d71184',
    )


    def parse(self, response):
        for href in response.css('.news-list > li > h3 > a::attr(href)'):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_item)
        
        try:
            next_page = response.css('li.next > a::attr(href)')[0].extract()
            yield scrapy.Request(next_page, callback=self.parse)
        except:
            pass


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css(".article > h1").xpath('.//text()').extract()[0]
        item['date'] = response.css(".article > h3").xpath('.//text()').extract()[0]
        item['body'] = " ".join(response.css(".txt").xpath('.//text()').extract())
        item['link'] = response.url
        item['country'] = 'slovenia'
        yield item



