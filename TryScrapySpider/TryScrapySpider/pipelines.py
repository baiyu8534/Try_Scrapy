# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
collection = client["Aqdy"]["shebao"]


class TryscrapyspiderPipeline(object):

    def open_spider(self,spider):
        # 爬虫开启时执行一次
        pass

    def close_spider(self,spider):
        # 爬虫结束时执行一次
        pass

    def process_item(self, item, spider):
        item["catch_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return item


class TryscrapyspiderPipeline1(object):
    def process_item(self, item, spider):
        print(item)
        collection.insert(dict(item))
        return item
