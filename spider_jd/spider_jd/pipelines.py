# -*- coding: utf-8 -*-
from spider_jd.items import *
from scrapy.exceptions import DropItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SpiderJdPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,SpiderCommentItem):
            print(item['content'])
            raise DropItem()


        if isinstance(item,SpiderJdItem):
            print(item['sku_id'])
            return item
