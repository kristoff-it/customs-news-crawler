# -*- coding: utf-8 -*-
import scrapy


class Item(scrapy.Item):
    country = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field()
    link = scrapy.Field()

class RomaniaSpider(scrapy.Spider):
    name = "romania"
    allowed_domains = ["customs.ro"]
    start_urls = (
        'https://www.customs.ro/ro/comunicate_de_presa.aspx',
    )

    # def make_requests_from_url(self, url):
    #        request = super(BosniaSpider, self).make_requests_from_url(url)
    #        request.cookies['filth.localization'] = 'en'
    #        return request

    def parse(self, response):
        elems = response.css('#p_ctl03_pnlArticleList > table > tr')
        i = 0

        while i < len(elems):
                i += 1
                item = Item()
                item['title'] = ''
                item['date'] = " ".join([x for x in elems[i - 1].xpath('.//text()').extract() if len(x.strip()) > 1])
                item['body'] = " ".join([x for x in elems[i].xpath('.//text()').extract() if len(x.strip()) > 1])
                item['link'] = response.urljoin(" ".join(elems[i].css('a::attr(href)').extract()))
                item['country'] = 'romania'
                i += 2
                yield item

        if len(elems) > 1:
            form_viewstate = response.css('#aspnetForm > div > [name=__VIEWSTATE]::attr(value)').extract()
            eventtartget = "p$ctl03$pgrArticles$Next"
            yield scrapy.http.FormRequest(response.url, formdata={'__EVENTTARGET':eventtartget, '__EVENTARGUMENT':'', '__VIEWSTATE': form_viewstate, "p$ctl02$txtSearchQuery":"cuvinte cheie", "p$ctl06$txtName":"Nume", "p$ctl06$txtEmail":"Adresa email", "p$MainContentClass":"windowHeader"}, callback=self.parse)



        



