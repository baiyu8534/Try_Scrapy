# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TryscrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = scrapy.Field()
    movie_actor = scrapy.Field()
    movie_jpg = scrapy.Field()
    movie_info_url = scrapy.Field()
    catch_time = scrapy.Field()
    add_time = scrapy.Field()
    thunder = scrapy.Field()
    http_download_url = scrapy.Field()
    pass
