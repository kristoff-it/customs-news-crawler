# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class PolandSpider(scrapy.Spider):
    name = "poland"
    allowed_domains = ["mf.gov.pl"]
    start_urls = (
        'http://www.mf.gov.pl/sluzba-celna/wiadomosci/aktualnosci?p_p_id=101_INSTANCE_2UWl&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_count=1&_101_INSTANCE_2UWl_delta=10&_101_INSTANCE_2UWl_keywords=&_101_INSTANCE_2UWl_advancedSearch=false&_101_INSTANCE_2UWl_andOperator=true&cur=1#p_p_id_101_INSTANCE_2UWl_',
        )

    #['http://customs.bg/bg/pubs/0?p={}'.format(i) for i in range(416)]

    def parse(self, response):
        for href in response.css('a.article-source-title::attr(href)'):
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_item)
        
        try:
            next_page = response.css('a[title=następna]::attr(href)')[0].extract()
            yield scrapy.Request(next_page, callback=self.parse)
        except:
            pass


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css('.bip-article-title').xpath('.//text()').extract()[0]
        item['date'] = response.css('.metadata-entry.metadata-publish-date').xpath('.//text()').extract()[2].strip()
        item['body'] = " ".join(response.css('.bip-article-content').xpath('.//text()').extract())
        item['link'] = response.url
        item['country'] = 'poland'
        yield item



