# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
collection = client["jd_book"]["ebook"]


class JdebookPipeline(object):
    def process_item(self, item, spider):
        print(item["book_name"])
        collection.insert(item)
        print("插入mongo成功")
        return item
