# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class AlbaniaSpider(scrapy.Spider):
    name = "albania"
    allowed_domains = ["dogana.gov.al"]
    start_urls = (
        'http://www.dogana.gov.al/arkiva-njoftime',
    )


    def parse(self, response):
        for href in response.css('article > header > h2 > a::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_item)
        
        try:
            next_page = response.urljoin(response.css('.pager-next > a::attr(href)')[0].extract())
            yield scrapy.Request(next_page, callback=self.parse)
        except:
            pass


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css(".page-title").xpath('.//text()').extract()[0]
        item['date'] = response.css(".date-display-single").xpath('.//text()').extract()[0]
        item['body'] = " ".join(response.css(".field-type-text-with-summary").xpath('.//text()').extract())
        item['link'] = response.url
        item['country'] = 'albania'
        yield item



