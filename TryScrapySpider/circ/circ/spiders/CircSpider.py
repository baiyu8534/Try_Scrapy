# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CircspiderSpider(CrawlSpider):
    name = 'CircSpider'
    allowed_domains = ['circ.gov.cn']
    start_urls = ['http://circ.gov.cn/web/site0/tab5240/module14430/page1.htm']

    # rules = (
    #     # 详情页的url
    #     Rule(LinkExtractor(allow=r'/web/site0/tab5240/info\d+\.htm'), callback='parse_item'),
    #     Rule(LinkExtractor(allow=r'/web/site0/tab5240/module14430/page\d+.htm'), follow=True),
    # )
    rules = (
        # 详情页的url
        Rule(LinkExtractor(allow=r'/web/site0/tab5240/info\d+\.htm'), callback='parse_item'),
    )
    def parse_item(self, response):
        item = {}
        item["title"] = re.findall("<!--TitleStart-->(.*?)<!--TitleEnd-->", response.body.decode())[0]
        item["publish"] = re.findall("发布时间：(20\d{2}-\d{2}-\d{2})", response.body.decode())[0]
        print(item)
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()

        return item
