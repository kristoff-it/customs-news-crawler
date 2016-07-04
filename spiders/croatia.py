# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class CroatiaSpider(scrapy.Spider):
    name = "croatia"
    allowed_domains = ["carina.gov.hr"]
    start_urls = (
        'https://carina.gov.hr/vijesti/8?trazi=1&tip=&tip2=&tema=&datumod=&datumdo=&pojam=&page=1',
        )
    def parse(self, response):
        for href in response.css('.news_item > a::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_item)
        
        try:
            next_page = response.urljoin(response.css('.news_page_nav').xpath(".//a[text()[contains(.,'Sljedeća »')]]").xpath(".//@href")[0].extract())
            yield scrapy.Request(next_page, callback=self.parse)
        except:
            pass


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css('#content > div > h1').xpath('.//text()').extract()[0].strip()
        item['date'] = response.css('.time_info').xpath('.//text()').extract()[0].strip()
        item['body'] = " ".join(response.css('.page_content').xpath('.//text()').extract()).strip()
        item['link'] = response.url
        item['country'] = 'croatia'
        yield item



