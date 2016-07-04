# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class FyromSpider(scrapy.Spider):
    name = "fyrom"
    allowed_domains = ["customs.gov.mk"]
    start_urls = (
        'http://www.customs.gov.mk/DesktopDefault.aspx?tabindex=0&tabid=187',
        )
    def parse(self, response):
        
        for row in response.css('.NewsTopOtherTitle'):
            href = row.css('.ItemTitle::attr(href)')[0]
            url = response.urljoin(href.extract())
            item = scrapy.Request(url, callback=self.parse_item)
            item.meta['date'] = row.css('.NewsTopOtherTitle > div > span').xpath('.//text()').extract()[0]
            yield item 

        form_viewstate = response.css('#Form1 > [name=__VIEWSTATE]::attr(value)').extract()
        
        if response.meta.get('first', True):
            # Next 10 pages
            for i in range(1, 10):
                next_page = scrapy.http.FormRequest(response.url, formdata={'__EVENTTARGET':"_ctl0:dgrNews:_ctl14:_ctl{}".format(i), '__EVENTARGUMENT':'', '__VIEWSTATE': form_viewstate}, callback=self.parse)
                next_page.meta['first'] = False
                yield next_page
            # Next pagegroup
            current_count = response.meta.get('count', 0)
            if  current_count < 60:
                next_group = scrapy.http.FormRequest(response.url, formdata={'__EVENTTARGET':"_ctl0:dgrNews:_ctl14:_ctl10", '__EVENTARGUMENT':'', '__VIEWSTATE': form_viewstate}, callback=self.parse)
                next_group.meta['count'] = current_count + 10
                yield next_group


    def parse_item(self, response):
        item = Item()
        item['title'] = response.css('#TitleField').xpath('.//text()').extract()[0].strip()
        item['date'] = response.meta['date']
        item['body'] = " ".join(response.css('#HtmlHolder').xpath('.//text()').extract()).strip()
        item['link'] = response.url
        item['country'] = 'fyrom'
        yield item



