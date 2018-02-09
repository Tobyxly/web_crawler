# -*- coding: utf-8 -*-
import scrapy
from spider_ckxx.items import CkxxItem
from scrapy_redis.spiders import RedisSpider

class CkxxbotSpider(scrapy.Spider):
    name = 'ckxxbot'
    start_urls = ['http://www.cankaoxiaoxi.com/china/szyw/1.shtml']
    BASE_URL = "http://www.cankaoxiaoxi.com/china/szyw/%d.shtml"

    pageno = 2
    def parse(self, response):

        items = response.selector.css('.txt-list-a.fz-14')
        sub_items = items[0].css('li')
        for item in sub_items:
            try:
                s_title = item.css('a::text').extract() #extract(): 返回被选择元素的unicode字符串
                s_link = item.css('a::attr(href)').extract()
                s_time = item.css('span::text').extract()
                n_item = CkxxItem()
                n_item['title'] = s_title[0]
                n_item['link'] = s_link[0]
                n_item['timestamp'] = s_time[0]

                yield n_item
            except:
                pass

        next_page = self.BASE_URL % self.pageno
        self.pageno += 1

        if self.pageno <5:
            yield scrapy.Request(next_page,callback=self.parse)