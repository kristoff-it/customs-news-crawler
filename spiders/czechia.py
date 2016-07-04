# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class CzechiaSpider(scrapy.Spider):
    name = "czechia"
    allowed_domains = ["celnisprava.cz"]
    start_urls = (
        'https://www.celnisprava.cz/cz/aktuality/Stranky/default.aspx',
        'https://www.celnisprava.cz/cz/aktuality/Stranky/archiv-aktualit-2015.aspx',
        'https://www.celnisprava.cz/cz/aktuality/Stranky/archiv2014.aspx',
        )
    def parse(self, response):
        for href in response.css('.dfwp-item > div > a::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_item)
        


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css('article > h1').xpath('.//text()').extract()[0].strip()
        item['date'] = " ".join(response.css('.publishedDateText').xpath('.//text()').extract()).strip()
        item['body'] = " ".join(response.css('.article-content').xpath('.//text()').extract()).strip()
        item['link'] = response.url
        item['country'] = 'czechia'
        yield item



