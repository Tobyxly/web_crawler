# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderJdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sku_id = scrapy.Field()
    sku_name = scrapy.Field()
    sku_price = scrapy.Field()
    sku_shop = scrapy.Field()

class SpiderCommentItem(scrapy.Item):
    sku_id = scrapy.Field()
    content = scrapy.Field()
    guid = scrapy.Field()
    creationTime = scrapy.Field()

    #def __str__(self):
    #    return 'guid:%s' % self['guid']

class GatheredInfo(scrapy.Item):
    sku_id = scrapy.Field()
    sku_name = scrapy.Field()
    sku_price = scrapy.Field()
    sku_shop = scrapy.Field()
    content = scrapy.Field()
    guid = scrapy.Field()
    creationTime = scrapy.Field()
