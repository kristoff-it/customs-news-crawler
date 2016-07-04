# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class SlovakiaSpider(scrapy.Spider):
    name = "slovakia"
    allowed_domains = ["financnasprava.sk"]
    years = [
        (2016, 7),
        (2015, 10),
        (2014, 10),
    ]
    start_urls = ['https://www.financnasprava.sk/sk/pre-media/tlacove-spravy/_{}/{}/k'.format(year, page) for year, year_range in years for page in range(1, year_range + 1)]


    def parse(self, response):
        for href in response.css('dl.newsArchiv').css('a.arr::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_item)


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css("#content > h1").xpath('.//text()').extract()[0]
        item['date'] = "".join(response.css("p.date").xpath('.//text()').extract()).strip()
        item['body'] = " ".join(response.css(".newsContent").xpath('.//text()').extract())
        item['link'] = response.url
        item['country'] = 'slovakia'
        yield item



