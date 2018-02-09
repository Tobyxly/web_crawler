# -*- coding: utf-8 -*-
#! /usr/bin/env python3
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from spider_jd.items import SpiderJdItem, SpiderCommentItem, GatheredInfo
import json
import re


class JdbotSpider(scrapy.Spider):
    name = 'jdbot'
    start_urls = ['http://search.jd.com/Search?keyword=%E5%BD%A9%E7%94%B5%27%20%27&enc=utf-8&page=1']

    BASE_URL = 'http://search.jd.com/Search?keyword=%E5%BD%A9%E7%94%B5&enc=utf-8&page='

    COMMENT_BASE_URL = 'http://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv15438' \
                       '&productId=%s&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'

    def parse_detail(self,response):
        self.logger.info('processing##########################')
        try:

            res = response.body.decode('gbk')
            pattern = res.strip()
            start = pattern.index("{")
            pattern = pattern[start:-2]
            obj = json.loads(pattern)

            for item in obj['comments']:
                citem = SpiderCommentItem() #citem对象是自定义的python字典
                citem['content'] = item['content']
                citem['creationTime'] = item['creationTime']
                citem['guid'] = item['guid']
                citem['sku_id'] = response.meta['sku_item']['sku_id']
                yield citem
        except:
            pass

    def get_pageno(self,url):
        import re
        m = re.search('page=(\d+)$',url)
        if m:
            return int(m.group(1))
        return 0


    def parse(self,response):
        url = response.url
        items = response.css('.gl-item')
        stock_item = SpiderJdItem()
        for item in items:
            try:
                sku_id = item.css('li::attr(data-sku)').extract_first()
                sku_name = item.css('.p-name a em::text').extract_first()
                sku_price = item.css('.p-price i::text').extract_first()
                sku_shop = item.css('.p-shop a::text').extract_first()

                stock_item['sku_id'] = sku_id
                stock_item['sku_name'] = sku_name
                stock_item['sku_price'] = sku_price
                stock_item['sku_shop'] = sku_shop
                yield stock_item
                yield scrapy.Request(JdbotSpider.COMMENT_BASE_URL % sku_id, meta={'sku_item': stock_item},
                                    callback=self.parse_detail)

                #回调函数，在处理完前一页的商品信息后继续处理每个商品的评论信息
                #scrapy的meta的作用就是在执行scrapy.Request()函数时把一些回掉函数中需要的数据传进去，meta必须是一个字典
                # yield scrapy.Request(JdbotSpider.COMMENT_BASE_URL % sku_id, meta={'sku_item': stock_item},
                #                      callback=self.parse_detail)

            except:
                 pass

        pageno = self.get_pageno(url)
        if pageno > 0 and pageno < 10:
            next_url = JdbotSpider.BASE_URL + str(pageno+2)
            yield scrapy.Request(next_url,callback=self.parse())