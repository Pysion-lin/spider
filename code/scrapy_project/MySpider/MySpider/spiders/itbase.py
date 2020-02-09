# -*- coding: utf-8 -*-
import scrapy
from MySpider.items import MyspiderItem

class ItbaseSpider(scrapy.Spider):
    name = 'itbase'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        name_list = response.xpath('//div[@class="li_txt"]')
        for name in name_list:
            item = MyspiderItem()
            item['name']=name.xpath('./h3/text()')[0].extract()
            item['title']=name.xpath('./h4/text()')[0].extract()
            item['desc']=name.xpath('./p/text()')[0].extract()
            yield item

