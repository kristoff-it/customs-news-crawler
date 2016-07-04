# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class BosniaSpider(scrapy.Spider):
    name = "bosnia"
    allowed_domains = ["new.uino.gov.ba"]
    start_urls = (
        'http://www.new.uino.gov.ba/bs/clanci/novosti',
    )

    def make_requests_from_url(self, url):
           request = super(BosniaSpider, self).make_requests_from_url(url)
           request.cookies['filth.localization'] = 'en'
           return request

    def parse(self, response):
        for button in response.css('.accordionButton'):
            date = button.css('strong')[0].xpath('.//text()')
            href = button.css('strong > a::attr(href)')[0]
            url = response.urljoin(href.extract())
            req = scrapy.Request(url, cookies={'filth.localization': 'en'}, callback=self.parse_item)
            req.meta['date'] = date.extract()[0]
            yield req
        # Single page for now
        # try:
        #     next_page = response.urljoin(response.css('.pager-next > a::attr(href)')[0].extract())
        #     yield scrapy.Request(next_page, callback=self.parse)
        # except:
        #     pass


    def parse_item(self, response):
        item = Item()
        item['title'] = ''
        item['date'] = response.meta['date']
        item['body'] = " ".join(response.css(".post_body").xpath('.//text()').extract())
        item['link'] = response.url
        item['country'] = 'bosnia'
        yield item



